"""
Correct unwanted background scattering on diffraction images
Author: Sergey Bobkov
"""

import os
from typing import Optional, List
import numpy as np
from numba import njit
from scipy.stats import norm as sp_norm
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from . import cxidata, pdfreport


def correct_background(input_file: str, max_background: int = 50,
                       overflow_level: Optional[int] = None, chunk_size: int = 100):
    """Correct background in input CXI file

    Keyword arguments:
    input_file -- CXI file
    max_background -- maximum background intensity
    overflow_level -- maximum intensity when detector is still linear
    chunk_size -- number of frames processed in one chunk
    """

    image_ids = cxidata.get_image_groups(input_file)

    if not image_ids:
        raise ValueError('No data in CXI file: {}'.format(input_file))

    _, size_y, size_x = cxidata.get_dataset_shape(input_file, image_ids[0], 'data')
    data_histogram = np.zeros((max_background, size_y, size_x), dtype=np.int32)

    for image_id in image_ids:
        data_shape = cxidata.get_dataset_shape(input_file, image_id, 'data')

        if data_shape[1:] != (size_y, size_x):
            raise ValueError('Data shape is different for image groups 1 and {}'.format(image_id))

        num_frames = data_shape[0]

        for start in range(0, num_frames, chunk_size):
            end = min(start+chunk_size, num_frames)
            data_chunk = cxidata.read_dataset(input_file, image_id, 'data', start, end)
            _add_chunk_to_histogram(data_chunk.astype(np.int32), data_histogram)

    background = _estimate_background(data_histogram)

    for image_id in image_ids:
        num_frames = cxidata.get_dataset_shape(input_file, image_id, 'data')[0]
        mask = cxidata.read_dataset(input_file, image_id, 'mask')

        for start in range(0, num_frames, chunk_size):
            end = min(start+chunk_size, num_frames)
            data_chunk = cxidata.read_dataset(input_file, image_id, 'data', start, end)

            new_data_chunk = data_chunk - background
            overflow_mask = (data_chunk > overflow_level)
            new_data_chunk[overflow_mask] = data_chunk[overflow_mask]
            new_data_chunk[np.logical_or(mask != 0, new_data_chunk < 0)] = 0

            cxidata.update_dataset(input_file, image_id, 'data', new_data_chunk, start, end)


@njit
def _add_chunk_to_histogram(data_chunk: np.ndarray, histogram: np.ndarray):
    """Compute histogram for chunk of data and add result to existing histogram

    Keyword arguments:
    data_chunk -- input chunk of data (n_frame, y, x)
    histogram -- existing histogram
    """
    max_val, size_y, size_x = histogram.shape
    n_frames = len(data_chunk)

    for i in range(n_frames):
        for y_coord in range(size_y):
            for x_coord in range(size_x):
                val = data_chunk[i, y_coord, x_coord]
                if val < max_val:
                    histogram[val, y_coord, x_coord] += 1


def _normal_pdf(x_val: float, mu_val: float, amplitude_scale: float, width_scale: float):
    return amplitude_scale*sp_norm(mu_val, width_scale).pdf(x_val)


def _estimate_background(data_histogram: np.ndarray):
    max_value, size_y, size_x = data_histogram.shape
    result = np.zeros((size_y, size_x), dtype=int)
    fit_range = np.arange(max_value)

    most_frequent_values = np.argmax(data_histogram, axis=0)

    # Save coordinates where most frequent values > 0
    y_vals, x_vals = np.nonzero(most_frequent_values)

    for y_val, x_val in zip(y_vals, x_vals):
        pixel_hist = data_histogram[:, y_val, x_val]
        pix_most_freq = most_frequent_values[y_val, x_val]

        # Fit gaussian
        start_mean = pix_most_freq
        start_std = pix_most_freq/5
        start_scale = pixel_hist[pix_most_freq]/_normal_pdf(pix_most_freq, start_mean, 1, start_std)
        pstart = [start_mean, start_scale, start_std]

        try:
            popt, _ = curve_fit(_normal_pdf, fit_range, pixel_hist, p0=pstart)
        except RuntimeError:    # Estimation fails
            popt = pstart

        result[y_val, x_val] = max(np.floor(popt[0]), 0) # Background cannot be negative

    return result


def compute_mean_data(filename: str):
    """Compute mean image for CXI file

    Keyword arguments:
    filename -- CXI file

    Return:
    mean_image -- mean image
    """

    image_ids = cxidata.get_image_groups(filename)

    sum_stack = []
    num_frames_stack = []

    for image_id in image_ids:
        data_shape = cxidata.get_dataset_shape(filename, image_id, 'data')
        sum_data = cxidata.compute_dataset_sum(filename, image_id, 'data', axis=0)
        num_frames_stack.append(data_shape[0])
        sum_stack.append(sum_data)

    mean_image = np.stack(sum_stack).sum(axis=0) / np.array(num_frames_stack).sum()

    return mean_image


def _create_report_fig(old_mean_data: np.ndarray, new_mean_data: np.ndarray):
    """Plot figure for PDF report"""
    background = old_mean_data - new_mean_data

    fig, axis = plt.subplots(1, 3, figsize=(15, 10), dpi=200)
    pdfreport.plot_image(old_mean_data, axis[0], logscale=False)
    axis[0].set_title('Original mean image')
    pdfreport.plot_image(new_mean_data, axis[1], logscale=False)
    axis[1].set_title('Corrected mean image')
    pdfreport.plot_image(background, axis[2], logscale=False)
    axis[2].set_title('Estimated background')

    return fig


def generate_report(input_files: List[str], old_mean_list: List[np.ndarray],
                    new_mean_list: List[np.ndarray], report_path: str) -> None:
    """Create PDF report

    Keyword arguments:
    input_files -- paths of input CXI file
    old_mean_list -- list of mean data for files before correction
    new_mean_list -- list of mean data for files after correction
    report_path -- path for result pdf file
    """
    assert len(input_files) == len(old_mean_list)
    assert len(input_files) == len(new_mean_list)

    rep = pdfreport.ReportWriter(report_path)

    for fname, old_mean_data, new_mean_data in zip(input_files, old_mean_list, new_mean_list):
        fig = _create_report_fig(old_mean_data, new_mean_data)
        fig.suptitle(os.path.basename(fname), fontsize=20)
        rep.save_figure(fig)

    rep.close()
