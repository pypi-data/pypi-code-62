"""
Scripts for estimation of particle size for diffraction images in CXI file
Author: Sergey Bobkov
"""

from typing import Tuple
import numpy as np
from numba import njit, prange
from scipy import ndimage
from scipy.signal import argrelmin

from . import cxidata, sphere


def compute_psd_data(input_file: str, radius: int = 0, angular_data_ratio: float = 1,
                     chunk_size: int = 100) -> None:
    """Compute Power Spectral Density for images in CXI file and save it in 'psd/data'

    Keyword arguments:
    input_file -- input CXI file
    radius -- outer radius for PSD calculation
    angular_data_ratio -- ratio of angular data that should be considered
    pds_data_name -- dataset name to save result [default: "psd/data"]
    chunk_size -- number of frames processed in one chunk
    """

    pds_data_name = "psd/data"

    image_ids = cxidata.get_image_groups(input_file)
    for image_id in image_ids:
        data_shape = cxidata.get_dataset_shape(input_file, image_id, 'data')
        num_frames = data_shape[0]
        mask = cxidata.read_dataset(input_file, image_id, 'mask')
        image_center = cxidata.read_dataset(input_file, image_id, 'image_center')

        if radius == 0:
            radius = _max_angle_distance(data_shape[1:], image_center)

        if pds_data_name in cxidata.get_names(input_file, image_id):
            cxidata.delete_dataset(input_file, image_id, pds_data_name)

        cxidata.create_dataset(input_file, image_id, pds_data_name, (num_frames, radius), float)

        if angular_data_ratio < 1:
            proj_data = _prepare_polar_projection(mask.shape, radius)
            polar_mask = _apply_polar_projection(proj_data, mask, image_center, cval=1)

        for start in range(0, num_frames, chunk_size):
            end = min(start+chunk_size, num_frames)
            data_chunk = cxidata.read_dataset(input_file, image_id, 'data', start, end)
            psd_buffer = np.zeros((end - start, radius))

            if angular_data_ratio == 1:
                _compute_psd_array_numba(data_chunk, mask,
                                         image_center, radius,
                                         psd_buffer)
            else:
                for i in range(end - start):
                    polar_data = _apply_polar_projection(proj_data, data_chunk[i],
                                                         image_center, cval=0)
                    polar_data[polar_mask] = 0
                    psd_buffer[i] = _compute_psd_polar(polar_data, polar_mask,
                                                       angular_data_ratio)

            cxidata.update_dataset(input_file, image_id, pds_data_name, psd_buffer, start, end)


def estimate_size(input_file: str, wavelength: float, distance: float, pixel_size: float,
                  r_min: int = 0, r_max: int = 0, interp: int = 5,
                  size_min: float = 0, size_max: float = 0, num_size: int = 300) -> None:
    """Estimate size of particles by PSD data in 'psd/data'

    Keyword arguments:
    input_file -- input CXI file
    wavelength -- radiation wavelenght (Angstrom)
    distance -- distance between detector and interaction point (m)
    pixel_size -- size of one detector pixel (m)
    r_min -- inner radius for PSD fitting (pix)
    r_max -- outer radius for PSD fitting (pix)
    interp -- interpolation factor to avoid collapse of sphere form-factor oscilation
    size_min -- minimum particle size (Angstrom)
    size_max -- maximum particle size (Angstrom)
    num_size -- number of tested sizes within size range
    """
    freq_step = pixel_size/(wavelength*distance)

    image_ids = cxidata.get_image_groups(input_file)
    for image_id in image_ids:
        psd_data = cxidata.read_dataset(input_file, image_id, "psd/data")

        names = cxidata.get_names(input_file, image_id)

        for dset_name in ["psd/scale", "psd/fit_diff", "psd/size_range",
                          "psd/size", "psd/size_score"]:
            if dset_name in names:
                cxidata.delete_dataset(input_file, image_id, dset_name)

        if r_min == 0:
            beamstop = np.argmax(psd_data.max(axis=0) > 0)
            r_min = beamstop + 2
        if r_max == 0:
            r_max = psd_data.shape[1]

        if size_min == 0:
            size_min = sphere.compute_size(psd_data.shape[1]//2, freq_step)
        if size_max == 0:
            size_max = sphere.compute_size(6, freq_step)

        fit_result = _estimate_size_psd_sphere(psd_data, freq_step, size_min, size_max,
                                               r_min, r_max, interp, num_size)

        size = np.zeros(len(psd_data))
        size_score = np.ones(len(psd_data))

        for j, frame_fit_diff in enumerate(fit_result['fit_diff']):
            local_min, score = _get_fit_optimum(frame_fit_diff)
            size[j] = fit_result['size_range'][local_min]
            size_score[j] = score

        cxidata.save_dataset(input_file, image_id, "psd/scale", fit_result['scale'])
        cxidata.save_dataset(input_file, image_id, "psd/fit_diff", fit_result['fit_diff'])
        cxidata.save_dataset(input_file, image_id, "psd/size_range", fit_result['size_range'])
        cxidata.save_dataset(input_file, image_id, "psd/size", size)
        cxidata.save_dataset(input_file, image_id, "psd/size_score", size_score)


def correct_size(input_file: str, size_multiplier: float) -> None:
    """Correct size in CXI file by factor of size_multiplier

    Keyword arguments:
    input_file -- input CXI file
    size_multiplier -- correction factor
    """

    name = "psd/size"

    image_ids = cxidata.get_image_groups(input_file)
    for image_id in image_ids:
        size = cxidata.read_dataset(input_file, image_id, name)
        size *= size_multiplier
        cxidata.update_dataset(input_file, image_id, name, size)


def _max_angle_distance(frame_shape: Tuple[int, int], center: np.ndarray) -> int:
    """Calculate distance from center to farest angle for frame

    Keyword arguments:
    frame_shape -- frame shape (size_y, size_x)
    center -- center coordinates (x, y)

    Return:
    distance -- integer distance value
    """

    max_x_distance = max(center[0], frame_shape[1] - center[0])
    max_y_distance = max(center[1], frame_shape[0] - center[1])
    distance = np.sqrt(max_x_distance**2 + max_y_distance**2)
    return int(np.floor(distance))


@njit(fastmath=True)
def _compute_psd_numba(image_data, mask_data, image_center, r_max):
    psd = np.zeros(r_max)
    work_pixels = np.zeros(r_max)

    start_x = int(np.round(image_center[0]) - (r_max + 1))
    end_x = int(np.round(image_center[0]) + (r_max + 1))

    start_y = int(np.round(image_center[1]) - (r_max + 1))
    end_y = int(np.round(image_center[1]) + (r_max + 1))

    for i in range(start_y, end_y + 1):
        y_dist = i - image_center[1]
        for j in range(start_x, end_x + 1):
            x_dist = j - image_center[0]

            r_value = int(np.round(np.sqrt(x_dist**2 + y_dist**2)))

            if r_value >= r_max:
                continue

            if 0 <= j < image_data.shape[1] and 0 <= i < image_data.shape[0]:
                if mask_data[i, j] == 0:
                    work_pixels[r_value] += 1
                    psd[r_value] += image_data[i, j]

    for i in range(r_max):
        if work_pixels[i] > 0:
            psd[i] /= work_pixels[i]

    return psd


@njit(parallel=True)
def _compute_psd_array_numba(image_data, mask_data, image_center, r_max, out_psd):
    num_frames = len(image_data)
    for i in prange(num_frames):    # pylint: disable=E1133
        out_psd[i] = _compute_psd_numba(image_data[i], mask_data, image_center, r_max)


def _prepare_polar_projection(data_shape, r_max, size_r=0, size_angle=500):
    """Create proj_data that can be used to speed-up multiple polar projections

    Keyword arguments:
    data_shape -- shape of input data
    limit -- outer limit for image: 'corner', 'edge' or distance in pixels from center
    nr -- radial resolution of result, by default equal distance from center in pixels
    nt -- angular resolution of result, by default 500 angles.

    Return:
    proj_data -- dict to input in _apply_polar_projection()
    """
    size_y, size_x = data_shape[:2]

    r_min = 0
    t_max = np.pi
    t_min = -np.pi

    if size_r == 0:
        size_r = int(r_max)

    r_i = np.linspace(r_min, r_max, size_r, endpoint=False)
    theta_i = np.linspace(t_min, t_max, size_angle, endpoint=False)
    theta_grid, r_grid = np.meshgrid(theta_i, r_i)

    x_grid = r_grid * np.cos(theta_grid)
    y_grid = r_grid * np.sin(theta_grid)

    x_grid, y_grid = x_grid.flatten(), y_grid.flatten()
    coords = np.vstack((y_grid, x_grid))

    proj_data = {'coords': coords,
                 'size_x': size_x,
                 'size_y': size_y,
                 'size_r': size_r,
                 'size_angle': size_angle}

    return proj_data


def _apply_polar_projection(proj_data, image_data, image_center=None, cval=0):
    """Apply polar projection by proj_data dict to speed-up multiple polar projections

    Keyword arguments:
    proj_data -- output of _prepare_polar_projection()
    image_data -- input 2d image
    image_center -- center position of polar coordinate system, in pixels
    cval -- default value to fill missed areas

    Return:
    result -- 2d image in polar coordinates with shape = (size_r, size_angle)
    """
    assert isinstance(proj_data, dict)

    if image_center is None:
        image_center = (proj_data['size_x']/2.0-0.5, proj_data['size_y']/2.0-0.5)

    coords = proj_data['coords'].copy()

    coords[0] += image_center[1] # Y coords
    coords[1] += image_center[0] # X coords

    mapped_data = ndimage.map_coordinates(image_data, coords, order=0, cval=cval)

    return mapped_data.reshape((proj_data['size_r'], proj_data['size_angle']))


def _compute_psd_polar(polar_data, polar_mask, angular_data_ratio):
    angular_sum = polar_data.sum(axis=0)
    angle_filter = (angular_sum > angular_sum.max() * (1 - angular_data_ratio))

    psd = polar_data[:, angle_filter].sum(axis=1).astype(np.float)
    psd_norm = (polar_mask[:, angle_filter] == 0).sum(axis=1)
    psd[psd_norm == 0] = 0
    psd[psd_norm > 0] /= psd_norm[psd_norm > 0]

    return psd


def _estimate_size_psd_sphere(psd_data, freq_step, size_min, size_max,
                              r_min, r_max, interp, num_size):
    """Estimate particle size by fit of PSD data with spherical form factor

    Keyword arguments:
    psd -- input PSD data
    size_min -- minimum allowed particle size
    size_max -- maximum allowed particle size
    freq_step -- frequency increment for 1 pixex, equal to pixel_size/(wavelength*distance)
    r_min -- minimum radius (index of PSD array) used to fit
    r_max -- maximum radius (index of PSD array) used to fit
    interp -- interpolation factor to avoid collapse of low period oscilation
    num_size -- number of tested sizes within size range

    Return:
    result - dictionary with fitting result
             {"fit_diff", "size_range", "scale", "fit_x", "fit_base"}
    """

    num_frames = psd_data.shape[0]
    x_vals = np.arange(r_min, r_max)
    x_interp = np.arange(r_min, r_max, 1/interp)

    frequency_interp = x_interp*freq_step

    size_range = np.linspace(size_min, size_max, num_size)
    # r_mid_range = size_range*(1+np.sqrt(5))/(2*np.sqrt(10+2*np.sqrt(5)))

    fit_base = np.zeros((num_size, frequency_interp.size))

    for i in range(num_size):
        fit = sphere.form_factor(frequency_interp, size_range[i]/2, 1)
        fit_base[i] = fit/fit.mean()

    fit_diff = np.zeros((num_frames, num_size))
    scale = np.zeros((num_frames,))

    for i in range(num_frames):
        data_to_fit = np.interp(x_interp, x_vals, psd_data[i, r_min:r_max])
        scale[i] = data_to_fit.mean()
        if scale[i] > 0:
            data_to_fit /= scale[i]
            fit_diff[i] = np.abs(fit_base - data_to_fit).sum(axis=1)
        else:
            # for 0 vector we set best fit at minimal size value
            fit_diff[i] = 2
            fit_diff[i, 0] = 1

    return {'fit_diff':fit_diff, 'size_range':size_range, 'scale':scale,\
            'fit_x':x_interp, 'fit_base':fit_base}


def _get_fit_optimum(frame_fit_diff: np.ndarray) -> Tuple[int, float]:
    """ Get index of optimum fit and calculate fidelity score

    Keyword arguments:
    frame_fit_diff -- 1D array with fit values for one frame against size range

    Return:
    index -- index of frame_fit_diff with best fit
    score -- calculated fidelity score
    """
    local_min = argrelmin(frame_fit_diff, order=5, mode='wrap')[0]
    min_diff = frame_fit_diff[local_min]
    local_min = local_min[np.argsort(min_diff)]
    if local_min.size > 1:
        score = frame_fit_diff[local_min[1]] / frame_fit_diff[local_min[0]]
    else:
        score = 1

    return local_min[0], score
