#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute number of photons and lit-pixels for data in cxi dataset
Author: Sergey Bobkov
"""

import os
import sys
import shutil
import subprocess
import argparse
from tqdm import tqdm

from spi_processing.compute_photons import compute_photons


def main():
    parser = argparse.ArgumentParser(
        description="Compute number of photons and litpixels in CXI data")
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out', dest='output_dir', help="Output directory")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_dir = parser_args.output_dir

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    if output_dir:
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
        compute_photons(fname)


if __name__ == '__main__':
    main()
