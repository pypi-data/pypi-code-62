#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set image_center in CXI file
Author: Sergey Bobkov
"""

import os
import sys
import shutil
import subprocess
import argparse
import numpy as np
from tqdm import tqdm

from spi_processing import center, cxidata


def main():
    parser = argparse.ArgumentParser(description='Set image center in CXI data')
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out', dest='output_dir', help="Output directory")
    parser.add_argument('-x', dest='center_x', type=float, help="x coordinate (pixels)")
    parser.add_argument('-y', dest='center_y', type=float, help="y coordinate (pixels)")
    parser.add_argument('-z', dest='center_z', type=float, default=0, help="z coordinate (pixels)")
    parser.add_argument('-i', '--input', dest='input', metavar='FILE',
                        help='Copy beam position from CXI file')
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_dir = parser_args.output_dir
    center_x = parser_args.center_x
    center_y = parser_args.center_y
    center_z = parser_args.center_z
    input_file = parser_args.input

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

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

    if (input_file is None) == ((center_x is None) or (center_y is None)):
        parser.error("Define center position (x and y) or input CXI file")

    if (center_x is None) != (center_y is None):
        parser.error("Define both x and y positions or input CXI file")

    if input_file is not None:
        image_ids = cxidata.get_image_groups(input_file)
        names = cxidata.get_names(input_file, image_ids[0])
        if 'image_center' not in names:
            parser.error("Input CXI file miss image_center dataset")
        new_center = cxidata.read_dataset(input_file, image_ids[0], 'image_center')
    else:
        new_center = np.array([center_x, center_y, center_z])

    for fname in tqdm(input_files):
        center.save(fname, new_center)


if __name__ == '__main__':
    main()
