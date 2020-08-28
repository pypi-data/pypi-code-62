#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Correct background scattering in diffraction data in CXI files
Author: Sergey Bobkov
"""

import os
import sys
import shutil
import subprocess
import argparse
from tqdm import tqdm

from spi_processing import correct_background


def main():
    parser = argparse.ArgumentParser(
        description='Correct background scattering in diffraction data in CXI files')
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out', dest='output_dir', help="Output directory")
    parser.add_argument('-M', '--max', default=50, help="Maximum background intensity")
    parser.add_argument('-O', '--overflow', default=70,
                        help="Maximum intensity when detector is still linear")
    parser.add_argument('-r', '--report', default="correct_background_report.pdf",
                        help="Report file")
    parser.add_argument('--no-correct', dest='nocorr', action='store_true',
                        help="Do not correct data, generate report for already corrected data")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_dir = parser_args.output_dir
    max_background = parser_args.max
    overflow_level = parser_args.overflow
    report_path = parser_args.report
    nocorr = parser_args.nocorr

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    old_mean_list = []
    new_mean_list = []

    if nocorr:
        if not output_dir:
            parser.error("--no-correct require OUTPUT_DIR")

        new_input_files = []
        for fname in input_files:
            new_fname = os.path.join(output_dir, os.path.basename(fname))
            new_input_files.append(new_fname)
            if not os.path.isfile(new_fname):
                parser.error("Output file {} doesn't exist".format(fname))

        sys.stderr.write("Reading files\n")
        for i in tqdm(range(len(input_files))):
            old_mean_list.append(correct_background.compute_mean_data(input_files[i]))
            new_mean_list.append(correct_background.compute_mean_data(new_input_files[i]))
    else:
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
            old_mean_list.append(correct_background.compute_mean_data(fname))
            correct_background.correct_background(fname, max_background, overflow_level)
            new_mean_list.append(correct_background.compute_mean_data(fname))

    sys.stderr.write("Generating report...")
    correct_background.generate_report(input_files, old_mean_list, new_mean_list, report_path)
    sys.stderr.write("Done\n")


if __name__ == '__main__':
    main()
