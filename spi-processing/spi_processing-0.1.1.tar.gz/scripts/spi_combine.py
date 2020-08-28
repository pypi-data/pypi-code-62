#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Combine several CXI files into one, combine datasets when possible
Author: Sergey Bobkov
"""

import os
import argparse

from spi_processing import combine


def main():
    parser = argparse.ArgumentParser(description="Combine several CXI files into one, combine datasets when possible")
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-o', '--out_file', dest='output_file', required=True, help="Output file")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    output_file = parser_args.output_file

    for fname in input_files:
        if not os.path.exists(fname) or not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    if os.path.exists(output_file):
        parser.error("File {} already exists".format(output_file))

    combine.combine_files(input_files, output_file)


if __name__ == '__main__':
    main()
