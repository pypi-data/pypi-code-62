"""Module for describing different kinds of noise."""
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from copy import copy
from abtem.measure import Measurement


def _pixel_times(dwell_time, flyback_time, shape):
    """
    Pixel times internal function

    Function for calculating scan pixel times.

    Parameters
    ----------
    dwell_time : float
        Dwell time on a single pixel in s.
    flyback_time : float
        Flyback time for the scanning probe at the end of each scan line in s.
    shape : two ints
        Dimensions of a scan in pixels.
    """

    line_time = (dwell_time * shape[1]) + flyback_time
    slow_time = np.tile(np.linspace(line_time, shape[0] * line_time, shape[0])[:, None], (1, shape[1]))
    fast_time = np.tile(np.linspace((line_time - flyback_time) / shape[1],
                                    line_time - flyback_time, shape[1]), (shape[0], 1))
    return slow_time + fast_time


def _single_axis_distortion(time, max_frequency, num_components):
    """
    Single axis distortion internal function

    Function for emulating a scan distortion along a single axis.

    Parameters
    ----------
    time : float
        Time constant for the distortion in s.
    max_frequency : float
        Maximum noise frequency in 1 / s.
    num_components: int
        Number of frequency components.
    """

    frequencies = np.random.rand(num_components, 1, 1) * max_frequency
    amplitudes = np.random.rand(num_components, 1, 1) / np.sqrt(frequencies)
    displacements = np.random.rand(num_components, 1, 1) / frequencies
    return (amplitudes * np.sin(2 * np.pi * (time + displacements) * frequencies)).sum(axis=0)


def _make_displacement_field(time, max_frequency, num_components, rms_power):
    """
    Displacement field creation internal function

    Function to create a displacement field to emulate 2D scan distortion.

    Parameters
    ----------
    time : float
       Time constant for the distortion in s.
    max_frequency : float
       Maximum noise frequency in 1 / s.
    num_components : int
       Number of frequency components.
    rms_power : float
       Root-mean-square power of the distortion.
    """

    profile_x = _single_axis_distortion(time, max_frequency, num_components)
    profile_y = _single_axis_distortion(time, max_frequency, num_components)

    x_mag_deviation = np.gradient(profile_x, axis=1)
    y_mag_deviation = np.gradient(profile_y, axis=0)

    frame_mag_deviation = (1 + x_mag_deviation) * (1 + y_mag_deviation) - 1
    frame_mag_deviation = np.sqrt(np.mean(frame_mag_deviation ** 2))

    # 235.5 = 2.355 * 100 %; 2.355 converts from 1/e width to FWHM

    profile_x *= rms_power / (235.5 * frame_mag_deviation)
    profile_y *= rms_power / (235.5 * frame_mag_deviation)

    return profile_x, profile_y


def _apply_displacement_field(image, distortion_x, distortion_y):
    """
    Displacement field applying function

    Function to apply a displacement field to an image.

    Parameters
    ----------
    image : ndarray
        Image array.
    distortion_x : ndarray
        Displacement field along the x axis.
    distortion_y : ndarray
        Displacement field along the y axis.
    """

    x = np.arange(0, image.shape[0])
    y = np.arange(0, image.shape[1])

    interpolating_function = RegularGridInterpolator([x, y], image, fill_value=None)

    y, x = np.meshgrid(y, x)
    p = np.array([(x + distortion_x).ravel(), (y + distortion_y).ravel()]).T

    p[:, 0] = np.clip(p[:, 0], 0, x.max())
    p[:, 1] = np.clip(p[:, 1], 0, y.max())

    warped = interpolating_function(p)
    return warped.reshape(image.shape)


def add_scan_noise(measurement: Measurement, dwell_time: float, flyback_time: float, max_frequency: float,
                   rms_power: float, num_components: int = 200):
    """
    Scan noise function

    Function to add scan noise to an image.

    Parameters
    ----------
    image : ndarray
        Image array.
    dwell_time : float
        Dwell time on a single pixel in s.
    flyback_time : float
        Flyback time for the scanning probe at the end of each scan line in s.
    max_frequency : float
        Maximum noise frequency in 1 / s.
    rms_power : float
        Root-mean-square power of the distortion.
    num_components : int, optional
        Number of frequency components.
    """

    measurement = measurement.copy()
    time = _pixel_times(dwell_time, flyback_time, measurement.array.T.shape)
    displacement_x, displacement_y = _make_displacement_field(time, max_frequency, num_components, rms_power)
    array = _apply_displacement_field(measurement.array[:].T, displacement_x, displacement_y)
    measurement.array[:] = array.T
    return measurement


def poisson_noise(measurement, dose):
    """Function to describe Poisson noise for a given measurement with an irradiation dose given in electrons / Å^2."""
    pixel_area = np.product([calibration.sampling for calibration in measurement.calibrations])
    measurement = measurement.copy()
    array = measurement.array
    measurement.array[:] = array / np.sum(array) * dose * pixel_area * np.prod(array.shape)
    measurement.array[:] = np.random.poisson(array).astype(np.float)
    return measurement
