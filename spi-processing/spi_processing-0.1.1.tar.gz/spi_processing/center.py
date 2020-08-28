"""
Scripts for estimation of image center for diffraction images in CXI file
Author: Sergey Bobkov
"""

import os
from typing import List
import numpy as np
from scipy.optimize import least_squares, brute
from scipy.spatial import distance as sp_distance
import matplotlib.pyplot as plt

from . import cxidata, pdfreport, sphere
from .particle_size import _compute_psd_numba


def save(input_file: str, image_center: np.ndarray) -> None:
    """Save image_center position if CXI file

    Keyword arguments:
    input_file -- name of file
    image_center -- numpy array with center coordinates [x, y, z] in pixels
    """

    dset_name = 'image_center'

    if not isinstance(image_center, np.ndarray) or image_center.shape != (3,):
        raise ValueError("Expected numpy array with 3 elements")

    image_ids = cxidata.get_image_groups(input_file)

    for image_id in image_ids:
        if dset_name in cxidata.get_names(input_file, image_id):
            cxidata.delete_dataset(input_file, image_id, dset_name)

        cxidata.save_dataset(input_file, image_id, dset_name, image_center)


def estimate_center_by_rotate_symmetry(data: np.ndarray, mask: np.ndarray, min_points: int = 20,
                                       relative_distance_lim: float = 0.1, loss: str = 'linear'):
    """Estimate beam position by rotational symmetry
    (equal distance to points with equal intensity)

    Keyword arguments:
    data -- input image
    mask -- mask of good pixels, 0 - good, other values - bad.
    min_points -- minimal number of point with equal intensity to consider that intensity
    relative_distance_lim -- maximum allowed difference of relative distance to points
    loss -- loss parameter for scipy.optimize.least_squares
            ('linear', 'soft_l1', 'huber', 'cauchy', 'arctan')
    """

    if not isinstance(data, np.ndarray) or data.ndim != 2:
        raise ValueError("Expected 2D numpy array for 'data'")

    if not isinstance(mask, np.ndarray) or mask.ndim != 2:
        raise ValueError("Expected 2D numpy array for 'mask'")

    if not np.issubdtype(data.dtype, np.integer):
        raise ValueError("Expected integer dtype for data")

    if mask.shape != data.shape:
        raise ValueError("'mask' shape does not fit with 'data'")

    size_y, size_x = data.shape

    x_range = np.arange(size_x)
    y_range = np.arange(size_y)
    x_coord, y_coord = np.meshgrid(x_range, y_range)

    mask = mask.flatten()
    good_pixels = (mask == 0)
    x_coord = x_coord.flatten()[good_pixels]
    y_coord = y_coord.flatten()[good_pixels]
    intensity = data.flatten()[good_pixels]

    center_stack = []

    vals, counts = np.unique(intensity, return_counts=True)

    for val, count in zip(vals, counts):
        if count < min_points:
            continue

        sel_x = x_coord[intensity == val]
        sel_y = y_coord[intensity == val]
        points = np.vstack([sel_x, sel_y]).T
        try:
            center = _fit_equal_distance(points, loss)
        except ValueError:
            continue

        cdist = sp_distance.cdist([center], points)[0]
        mean_distance = cdist.mean()
        max_diff = np.abs(cdist - mean_distance).max()

        if max_diff > relative_distance_lim*mean_distance or \
                max_diff > relative_distance_lim*max(size_x, size_y):
            continue

        center_stack.append([center[0], center[1], 0])

    if not center_stack:
        raise ValueError("Cannot find suited intensity values")

    center_stack = np.array(center_stack)
    center = center_stack.mean(axis=0)
    return np.round(center, decimals=1)


def refine_center_by_sphere_pattern(data: np.ndarray, mask: np.ndarray,
                                    wavelength: float, distance: float, pixel_size: float,
                                    start_center: np.ndarray, start_size: float,
                                    max_shift: int = 5, radius: int = 128) -> np.ndarray:
    """Search for center position with best fit between image and sphere scattering pattern

    Keyword arguments:
    data -- input image
    mask -- mask of good pixels, 0 - good, other values - bad.
    wavelength -- radiation wavelenght (Angstrom)
    distance -- distance between detector and interaction point (m)
    pixel_size -- size of one detector pixel (m)
    start_center -- position of center to start with (pixels)
    start_size -- starting size a sphere
    max_shift -- maximum difference between strating center and the result, affects performance
    radius -- maximum radius in pixels, that are taken into account

    Return:
    center -- position with best fitting quality
    """

    if not isinstance(data, np.ndarray) or data.ndim != 2:
        raise ValueError("Expected 2D numpy array for 'data'")

    if not isinstance(mask, np.ndarray) or mask.ndim != 2:
        raise ValueError("Expected 2D numpy array for 'mask'")

    if mask.shape != data.shape:
        raise ValueError("'mask' shape does not fit with 'data'")

    freq_step = pixel_size/(wavelength*distance)

    good_data = data[mask == 0]

    def center_fit_qual(center):
        psd_data = _compute_psd_numba(data, mask, center, r_max=radius)
        fit_res = sphere.refine_size(psd_data, start_size, freq_step)
        sphere_pattern = sphere.simulate_pattern(mask.shape, center, fit_res['r_mid'],
                                                 fit_res['scale'], freq_step)

        sphere_pattern = sphere_pattern[mask == 0]
        sphere_pattern *= good_data.mean()/sphere_pattern.mean()
        diff = np.abs(sphere_pattern - good_data).sum()
        return diff

    bounds = [(start_center[0]-max_shift, start_center[0]+max_shift),
              (start_center[1]-max_shift, start_center[1]+max_shift)]
    # result = differential_evolution(center_fit_qual, bounds)
    # center = np.round(result.x, decimals=1)

    center = brute(center_fit_qual, bounds, Ns=(max_shift*10 + 1)) # point every 0.2 pixels
    center = np.round(center, decimals=1)

    return np.array([center[0], center[1], 0])


def compute_sum_image(input_file: str) -> np.ndarray:
    """
    Compute sum of all images in 'data' in CXI file

    Keyword arguments:
    input_file -- input CXI files

    Return:
    sum_image -- 2D array with sum of all images
    """

    sum_image_stack = []
    image_ids = cxidata.get_image_groups(input_file)
    for image_id in image_ids:
        sum_image_stack.append(cxidata.compute_dataset_sum(input_file, image_id, 'data', 0))

    if not sum_image_stack:
        raise ValueError('Empty file: {}'.format(input_file))

    return np.stack(sum_image_stack).sum(axis=0)


def compute_common_mask(input_file: str) -> np.ndarray:
    """
    Compute mask with good pixels in 'mask' in all CXI file

    Keyword arguments:
    input_file -- input CXI file

    Return:
    mask -- 2D array with common mask
    """

    mask_stack = []
    image_ids = cxidata.get_image_groups(input_file)
    for image_id in image_ids:
        mask_stack.append(cxidata.read_dataset(input_file, image_id, 'mask'))

    if not mask_stack:
        raise ValueError('Empty file: {}'.format(input_file))

    return np.abs(np.stack(mask_stack)).min(axis=0)


def normalise_for_estimate(data: np.ndarray) -> np.ndarray:
    """
    Rescale image into 0-100 intensity range and round to integer values

    Keyword arguments:
    data -- input numpy array

    Return:
    result -- rescaled input converted into integer
    """

    max_val = data.max()
    if max_val > 100:
        data = 100 * (data/max_val)
    return np.round(data).astype(int)


def generate_report(input_files: List[str], sum_images: List[np.ndarray],
                    image_center_list: List[np.ndarray], report_path: str):
    """Create PDF report

    Keyword arguments:
    input_files -- paths of input CXI file
    sum_images -- list of sum_data for input files
    image_center_list -- list of image_center values for input files
    report_path -- path for result pdf file
    """

    assert len(input_files) == len(sum_images)
    assert len(input_files) == len(image_center_list)

    rep = pdfreport.ReportWriter(report_path)

    for fname, sum_image, image_center in zip(input_files, sum_images, image_center_list):
        fig = _create_report_fig(sum_image, image_center)
        fig.suptitle(os.path.basename(fname), fontsize=20)
        rep.save_figure(fig)

    rep.close()


def _create_report_fig(sum_data, image_center):
    """Plot figure for PDF report"""
    fig, axes = plt.subplots(figsize=(10, 10), dpi=200)
    pdfreport.plot_image(sum_data, axes)
    axes.plot(image_center[0], image_center[1], '+', color='r', markersize=30, linewidth=0.1)
    axes.add_artist(plt.Circle(image_center, 70, color='r', fill=False))
    axes.add_artist(plt.Circle(image_center, 50, color='r', fill=False))

    return fig


def _find_intersection(base_1, inc_1, base_2, inc_2):
    """Find the intersection point of two lines

    lines are defined as:
        base = (x, y)
        inc = (dx, dy)
        base + inc*t

    Keyword arguments:
    base_1, inc_1 -- first line
    base_2, inc_2 -- second line

    Return:
        res_x, res_y: coordinates of intersection
    """
    # x = x1 + dx1*t
    # y = y1 + dy1*t
    # y = y1 + (x - x1)*dy1/dx1
    # y = y2 + (x - x2)*dy2/dx2
    # (x - x1)*dy1/dx1 - (x - x2)*dy2/dx2 = y2 - y1
    # x*(dy1/dx1 - dy2/dx2) - x1*dy1/dx1 + x2*dy2/dx2 = y2 - y1
    # x = (y2 - y1 + (x1*dy1/dx1 - x2*dy2/dx2))/(dy1/dx1 - dy2/dx2)

    if inc_1[0] == 0:
        inc_1[0] = 1e-10
    if inc_2[0] == 0:
        inc_2[0] = 1e-10

    slope_1 = inc_1[1]/inc_1[0]
    slope_2 = inc_2[1]/inc_2[0]

    if slope_1 == slope_2:
        raise ValueError("Lines do not intersect (they are parallel)")

    res_x = (base_2[1] - base_1[1] + (base_1[0]*slope_1 - base_2[0]*slope_2))/(slope_1 - slope_2)
    res_y = base_1[1] + (res_x - base_1[0])*slope_1

    return res_x, res_y


def _triangulate(point_1, point_2, point_3):
    """Find center of a ring that pass through 3 points

    Keyword arguments:
    point_1 -- first point (x, y)
    point_2 -- second point (x, y)
    point_3 -- third point (x, y)

    Return:
    res_x, res_y -- center of a ring
    """
    # perpendicular bisector
    # y - (y1+y2)/2 = (x - (x1+x2)/2)*(-1*(x2 - x1)/(y2 - y1))
    # x1 = (x1+x2)/2
    # y1 = (y1+y2)/2
    # dx1 = -1*(x2 - x1)
    # dy1 = (y2 - y1)

    # bisector 1-2:
    base_1 = ((point_1[0] + point_2[0])/2, (point_1[1] + point_2[1])/2)
    inc_1 = ((point_2[1] - point_1[1]), -1*(point_2[0] - point_1[0]))
    # bisector 2-3:
    base_2 = ((point_2[0] + point_3[0])/2, (point_2[1] + point_3[1])/2)
    inc_2 = ((point_3[1] - point_2[1]), -1*(point_3[0] - point_2[0]))

    res_x, res_y = _find_intersection(base_1, inc_1, base_2, inc_2)

    return res_x, res_y


def _select_3_utmost_points(points):
    """Select 3 points from the list that are located farthest from each other

    Keyword arguments:
    points -- 2d array with shape (N, 2).
              points[;, 0] - x coorrdinates, points[;, 1] - y coorrdinates

    Return:
    idx1, idx2, idx3 -- indexes of 3 points in points array (first dimension)
    """
    idx1 = 0 # start from first

    # utmost from i1
    idx2 = np.argmax(sp_distance.cdist(points[[idx1]], points)[0])
    # utmost from i2
    idx3 = np.argmax(sp_distance.cdist(points[[idx2]], points)[0])
    # utmost both i2 and i3
    idx1 = np.argmax(np.amin(sp_distance.cdist(points[[idx2, idx3]], points), axis=0))

    return idx1, idx2, idx3


def _fit_equal_distance(points, loss):
    """Find center of a ring that pass as close as possible to all points,
    based on least_squares method from scipy.optimize

    Keyword arguments:
    points -- 2d array with shape (N, 2).
              points[;, 0] - x coorrdinates, points[;, 1] - y coorrdinates
    loss -- loss parameter for scipy.optimize.least_squares
            ('linear', 'soft_l1', 'huber', 'cauchy', 'arctan')

    Return:
    res.x -- coordinates array [x, y]
    """
    idx1, idx2, idx3 = _select_3_utmost_points(points)

    start_x, start_y = _triangulate(points[idx1], points[idx2], points[idx3])

    def fun_resud(center_point):
        cdist = sp_distance.cdist([center_point], points)[0]
        return np.abs(cdist - cdist.mean())

    res = least_squares(fun_resud, [start_x, start_y], loss=loss)

    return res.x
