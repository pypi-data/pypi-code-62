#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Estimate particle size for diffraction images by fitting of PSD with spherical form-factor
Author: Sergey Bobkov
"""

import os
import sys
import shutil
import subprocess
import argparse
import numpy as np
from tqdm import tqdm

from spi_processing import particle_size


def main():
    parser = argparse.ArgumentParser(description='Estimate particle size for diffraction images by fitting of PSD with spherical form-factor')
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out', dest='output_dir', help="Output directory")
    parser.add_argument('-p', '--percentage', type=float, default=1,
                        help="Percentage of used angular data, 1 for all, 0.1 for brightest 10 percent")
    parser.add_argument('-m', '--s_min', type=int, default=0,
                        help="Minimum possible size (Angstrom)")
    parser.add_argument('-M', '--s_max', type=int, default=0,
                        help="Maximum possible size (Angstrom)")
    parser.add_argument('-r', '--r_min', type=int, default=0,
                        help="Minimal fit radius (Pixels)")
    parser.add_argument('-R', '--r_max', type=int, default=0,
                        help="Maximum fit radius (Pixels)")
    parser.add_argument('-w', '--wavelength', type=float, required=True,
                        help="Radiation wavelength (Angstrom)")
    parser.add_argument('-d', '--distance', type=float, required=True,
                        help="Detector distance (meters)")
    parser.add_argument('--pix', dest='pixel', type=float, required=True,
                        help="Pixel size (meters)")
    parser.add_argument('-i','--interp', type=int, default=5,
                        help="Interpolation factor")
    parser.add_argument('-n', '--nsize', type=int, default=300,
                        help="Number of sizes tested within size range")
    parser.add_argument('--icosahedron', action='store_true',
                        help="Size of particle will be computed with assumption that it is a regular icosahedron")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_dir = parser_args.output_dir
    percentage = parser_args.percentage
    size_min = parser_args.s_min
    size_max = parser_args.s_max
    r_min = parser_args.r_min
    r_max = parser_args.r_max
    wavelength = parser_args.wavelength
    distance = parser_args.distance
    pixel_size = parser_args.pixel
    interp = parser_args.interp
    nsize = parser_args.nsize
    icosahedron = parser_args.icosahedron

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    if icosahedron:
        # r_mid = a/4 * (1 + sqrt(5))
        # r_outer = a/4 * sqrt(10 + 2*sqrt(5))
        size_multiplier = np.sqrt(10 + 2*np.sqrt(5)) / (1 + np.sqrt(5))
        if size_max is None:
            size_max /= size_multiplier
        if size_min is None:
            size_min /= size_multiplier

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        sys.stderr.write("Copying to output\n")
        os.makedirs(output_dir, exist_ok=True)
        new_input_files = []
        for fname in tqdm(input_files):
            new_fname = os.path.join(output_dir, os.path.basename(fname))
            shutil.copy(fname, new_fname)
            subprocess.call(["/bin/chmod", "u+w", new_fname])
            new_input_files.append(new_fname)
        input_files = new_input_files

    sys.stderr.write("Processing files\n")
    for fname in tqdm(input_files):
        particle_size.compute_psd_data(fname, r_max, percentage)
        particle_size.estimate_size(fname, wavelength, distance, pixel_size, r_min, r_max, interp,
                                    size_min, size_max, nsize)

        if icosahedron:
            particle_size.correct_size(fname, size_multiplier)


if __name__ == '__main__':
    main()
