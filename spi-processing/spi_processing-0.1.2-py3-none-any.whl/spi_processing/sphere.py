"""
Scripts for estimation of image center for diffraction images in CXI file
Author: Sergey Bobkov
"""

from typing import Tuple, Union
import numpy as np
from scipy.optimize import curve_fit


def simulate_pattern(shape: Tuple[int, int], center: np.ndarray,
                     sphere_r: float, scale: float, freq_step: float):
    """Construct 2d scattering pattern for sphere

    Keyword arguments:
    shape -- shape and mask of pattern to be constructed
    center -- position of scattering center (pixels)
    sphere_r -- mid radius of a sphere
    scale -- intensity value for pattern
    freq_step -- frequency increment for 1 pixel, equal to pixel_size/(wavelength*distance)

    Return:
    result -- 2d array with the simulated sphere scattering
    """
    y_range = np.arange(shape[0], dtype=np.float64)
    x_range = np.arange(shape[1], dtype=np.float64)

    x_grid, y_grid = np.meshgrid(x_range, y_range)
    x_grid -= center[0]
    y_grid -= center[1]

    # r_grid = np.round(np.sqrt(x_grid**2 + y_grid**2))
    # r_grid[mask_data != 0] = 0
    # vals, indices = np.unique(r_grid, return_inverse=True)
    # return sphere_form_factor(vals*one_pix_freq, sphere_mid, scale)[indices].reshape(r_grid.shape)

    r_grid = np.sqrt(x_grid**2 + y_grid**2)
    return form_factor(r_grid*freq_step, sphere_r, scale)


def refine_size(psd_data: np.ndarray, size_start: float, freq_step: float,
                r_min: int = 0, r_max: int = 0, return_fit: bool = False):
    """Refine particle size by fit of PSD data with spherical form factor
    Do not search for global minimum, find closest local minimum

    Keyword arguments:
    psd_data -- input PSD data
    size_start -- start size
    freq_step -- frequency increment for 1 pixex, equal to pixel_size/(wavelength*distance)
    r_min -- minimum radius (index of PSD array) used to fit
    r_max -- maximum radius (index of PSD array) used to fit

    Return:
    result -- dict with estimation results, 'r_mid' - radius of sphere with best fit,
              'size' - predicted size of a particle,
              'scale' - arbitrary intensity of a beam
    """
    if r_min == 0:
        beamstop = int(np.argmax(psd_data > 0))
        r_min = beamstop + 5
    if r_max == 0:
        r_max = len(psd_data)

    frequency_coord = np.arange(len(psd_data))*freq_step
    data_to_fit = psd_data[r_min:r_max]
    scale_start = data_to_fit.mean()/ \
                  form_factor(frequency_coord[r_min:r_max], size_start/2, 1).mean()

    pstart = [size_start/2, scale_start]

    try:
        popt, _ = curve_fit(form_factor,
                            frequency_coord[r_min:r_max],
                            data_to_fit,
                            p0=pstart, bounds=(0, np.inf))
    except RuntimeError:
        popt = pstart

    r_mid = popt[0]
    scale = popt[1]
    size = 2*r_mid
    result = {'r_mid':r_mid, 'size':size, 'scale':scale}

    if return_fit:
        radial_fit = np.array([form_factor(x, r_mid, scale) for x in frequency_coord])
        result['fit'] = radial_fit
        result['fit_start'] = r_min
        result['fit_end'] = r_max

    return result


def compute_size(first_min: int, freq_step: float):
    """Compute size of a sphere by position of first min in sphere form factor

    Keyword arguments:
    first_min_pix -- position of first minimum of form factor (pix)
    freq_step -- Spatial frequency for angle of one detector pixel (1/Angstrom)

    Return:
    size -- sphere size (pixel_size/(wavelength*distance)) (Angstrom)
    """

    return 4.5 / (np.pi*first_min*freq_step)


def form_factor(x_val: Union[float, np.ndarray], sphere_r: float, scale: float):
    """Calculate sphere form factor

    Keyword arguments:
    x -- spatial frequency
    r -- sphere radius
    scale -- intensity multiplier

    Return:
    res -- sphere form factor value
    """

    q_by_r = x_val*2*np.pi*sphere_r
    vol = (4/3)*np.pi*(sphere_r**3)
    with np.errstate(divide='ignore', invalid='ignore'):
        res = (scale/vol)*((3*vol*(np.sin(q_by_r) - q_by_r*np.cos(q_by_r))/q_by_r**3)**2)
    return np.nan_to_num(res)
