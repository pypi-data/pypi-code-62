#!python
# -*- coding: utf-8 -*-

"""
Estimate of image center for diffraction images in CXI file by rotational symmetry.
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
    parser = argparse.ArgumentParser(description="Estimate image center by rotational symmetry of powder image")
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out', dest='output_dir', help="Output directory")
    parser.add_argument('-s', '--same', action='store_true',
                        help="Consider all input files to have the same center position")
    parser.add_argument('-r', '--report', default="estimate_center_report.pdf",
                        help="Report file")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_dir = parser_args.output_dir
    same_pos = parser_args.same
    report_path = parser_args.report

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

    if same_pos:
        sum_data_stack = []
        mask_stack = []
        sys.stderr.write("Reading files\n")
        for fname in tqdm(input_files):
            sum_data_stack.append(center.compute_sum_image(fname))
            mask_stack.append(center.compute_common_mask(fname))

        sum_data = np.stack(sum_data_stack).sum(axis=0)
        sum_data = center.normalise_for_estimate(sum_data)

        # Get pixels that are good for all datasets
        mask = np.abs(np.stack(mask_stack)).min(axis=0)
        sys.stderr.write("Estimate center\n")
        image_center = center.estimate_center_by_rotate_symmetry(sum_data, mask)

        sys.stderr.write("Saving result\n")
        for fname in tqdm(input_files):
            center.save(fname, image_center)

        sys.stderr.write("Creating report\n")
        center.generate_report(["Summary image"], [sum_data], [image_center], report_path)
    else:
        sum_data_stack = []
        center_values = []
        sys.stderr.write("Processing files\n")
        for fname in tqdm(input_files):
            sum_data = center.compute_sum_image(fname)
            sum_data = center.normalise_for_estimate(sum_data)
            mask = center.compute_common_mask(fname)
            image_center = center.estimate_center_by_rotate_symmetry(sum_data, mask)
            center.save(fname, image_center)
            sum_data_stack.append(sum_data)
            center_values.append(image_center)

        sys.stderr.write("Creating report\n")
        center.generate_report(input_files, sum_data_stack, center_values, report_path)


if __name__ == '__main__':
    main()
