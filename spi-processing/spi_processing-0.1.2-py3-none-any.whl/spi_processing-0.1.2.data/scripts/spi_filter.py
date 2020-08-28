#!python
# -*- coding: utf-8 -*-

"""
Filter CXI file by dataset values
Author: Sergey Bobkov
"""

import os
import shutil
import tempfile
import argparse
import pandas as pd
from tqdm import tqdm

from spi_processing import combine, filtering, pdfreport


def main():
    parser = argparse.ArgumentParser(description='Filter CXI data by dataset values')
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-d', '--dset', dest='dset', required=True, help="Filtering dataset")
    parser.add_argument('-o', '--outdir', dest='output_dir', help="Output directory")
    parser.add_argument('--outfile', dest='output_file', help="Output file")
    parser.add_argument('-m', '--min', dest='min_value', type=float, help="Minimum size")
    parser.add_argument('-M', '--max', dest='max_value', type=float, help="Maximum size")
    parser.add_argument('-r', '--report', default='filter_report.pdf', help="Report file")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    dset_name = parser_args.dset
    output_dir = parser_args.output_dir
    output_file = parser_args.output_file
    min_value = parser_args.min_value
    max_value = parser_args.max_value
    report_path = parser_args.report

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    if output_dir is not None:
        if os.path.exists(output_dir) and not os.path.isdir(output_dir):
            parser.error("{} is not a directory".format(output_dir))
        elif not os.path.exists(output_dir):
            os.makedirs(output_dir)

    if output_file is not None:
        if os.path.exists(output_file):
            parser.error("File {} already exists".format(output_file))

    if report_path is not None:
        report_df = pd.DataFrame(columns=('Filename', 'Total images', 'Selected images'))

    tempdir = tempfile.TemporaryDirectory()
    if output_dir is None:
        output_dir = tempdir.name

    output_files = []
    for fname in tqdm(input_files):
        out_fname = os.path.join(output_dir, os.path.basename(fname))
        tot_n, sel_n = filtering.filter_file(fname, out_fname, dset_name, min_value, max_value)
        output_files.append(out_fname)

        if report_path is not None:
            report_df.loc[len(report_df)] = [os.path.split(fname)[1], tot_n, sel_n]

    if report_path is not None:
        report_df.loc[len(report_df)] = \
            ['Total', report_df.iloc[:, 1].sum(), report_df.iloc[:, 2].sum()]
        rep = pdfreport.ReportWriter(report_path)
        rep.save_table(report_df)
        rep.close()

    if output_file is not None:
        if len(output_files) == 1:
            shutil.move(output_files[0], output_file)
        else:
            combine.combine_files(output_files, output_file)

    tempdir.cleanup()


if __name__ == '__main__':
    main()
