"""
Processing of image data
Author: Sergey Bobkov
"""

import numpy as np
import scipy as sp
from scipy.fftpack import dct
from scipy.ndimage import map_coordinates


def get_symmetry_scores(image_data, center=None, num_components=50):
    """Compute vestor of symmetry scores by autocorrelation and fourier decomposition

    Keyword arguments:
    image_data -- 2D image array
    center -- tuple of center coordinates [default: center of image]
    num_components -- number of symmetry components in output

    Retuns:
    symmetry_scores -- 1D array of symmetry scores
    """

    if center is None:
        center = [x/2 for x in image_data.shape]

    edge_distance = min(image_data.shape[0] - center[0], center[0], \
                        image_data.shape[1] - center[1], center[1])

    polar_data = polar_projection(image_data, center, r_max=edge_distance, cval=0)
    polar_mask = polar_projection(image_data == 0, center, r_max=edge_distance, cval=1)
    r_mask = polar_mask.min(axis=1) == 0
    selected_data = polar_data[r_mask]

    corr_data = np.zeros((polar_data.shape[0], polar_data.shape[1]+1))
    for i, polar_line in enumerate(selected_data):
        corr_data[i, :] = sp.correlate(polar_line, np.concatenate((polar_line, polar_line)))

    corr_t = np.mean(corr_data, axis=0)
    corr_t /= corr_t[0]

    symmetry_scores = dct(corr_t, type=1)[::2]
    symmetry_scores[0] = 0
    symmetry_scores = symmetry_scores[:num_components]
    return symmetry_scores


def polar_projection(data, center, r_max=None, cval=None):
    """Compute polar projection

    Keyword arguments:
    data -- 2D image
    center -- tuple of center coordinates
    r_max -- maximum radius value in polar coordinates
    cval -- default value to fill missed areas

    Return:
    polar_data -- 2d image in polar coordinates with shape = (r_max, int(2*np.pi*r_max))
    """

    if r_max is None:
        x_max = max(data.shape[1] - center[1], center[1])
        y_max = max(data.shape[0] - center[0], center[0])
        r_max = np.sqrt(x_max**2 + y_max**2)

    r_max = int(r_max)

    r_i = np.arange(r_max)

    t_max = np.pi
    t_min = -np.pi
    t_num = int(2*np.pi*r_max)
    t_i = np.linspace(t_min, t_max, t_num, endpoint=False)

    t_grid, r_grid = np.meshgrid(t_i, r_i)

    x_grid = r_grid * np.cos(t_grid)
    y_grid = r_grid * np.sin(t_grid)

    x_grid, y_grid = x_grid.flatten(), y_grid.flatten()
    coords = np.vstack((y_grid + center[0], x_grid + center[1]))
    mapped_data = map_coordinates(data, coords, order=0, cval=cval)

    return mapped_data.reshape((r_max, t_num))
