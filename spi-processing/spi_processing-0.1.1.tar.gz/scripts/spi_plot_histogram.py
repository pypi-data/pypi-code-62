#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plot histogram for dataset in CXI file
Author: Sergey Bobkov
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tqdm import tqdm

from spi_processing import cxidata, pdfreport


def plot_histogram(data, dset_name, bins=100, x_lim=None, select=None):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)

    ax.hist(data, bins=bins, range=x_lim)
    ax.set_yscale('log')

    if select is not None:
        x_start = select[0]
        width = select[1] - select[0]
        rect = Rectangle((x_start,0), width, ax.get_ylim()[1],
                         hatch='///', color='C2', lw=1, fill=False)
        ax.add_artist(rect)

    ax.set_ylabel('Number of images')
    ax.set_xlabel(dset_name + ' values')
    return fig


def parse_range(range_str):
    if isinstance(range_str, str) and len(range_str.split(':')) == 2:
        return [int(val) for val in range_str.split(':')]
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description='Plot histogram of CXI dataset')
    parser.add_argument('files', metavar='FILE', nargs='+', help='Input files')
    parser.add_argument('-d', '--dset', required=True, help="Dataset")
    parser.add_argument('-r', '--range', metavar='START:END', type=parse_range,
                        help="Histogram range")
    parser.add_argument('-s', '--select', metavar='START:END', type=parse_range,
                        help="Selection range")
    parser.add_argument('-b', '--bins', type=int, default=100, help="Number of bins")
    parser.add_argument('-o', '--out_file', dest='output_file', default="data_histogram.pdf",
                        help="Output file")
    parser_args = parser.parse_args()

    input_files = parser_args.files
    dset_name = parser_args.dset
    hist_range = parser_args.range
    sel_range = parser_args.select
    bins = parser_args.bins
    output_file = parser_args.output_file

    for fname in input_files:
        if not os.path.isfile(fname):
            parser.error("File {} doesn't exist".format(fname))

    if os.path.exists(output_file):
        parser.error("File {} already exists".format(output_file))

    data_stack = []
    sys.stderr.write("Reading files\n")
    for fname in tqdm(input_files):
        image_ids = cxidata.get_image_groups(fname)
        for image_id in image_ids:
            data = cxidata.read_dataset(fname, image_id, dset_name)
            data_stack.append(data.flatten())

    data = np.concatenate(data_stack)

    sys.stderr.write("Creating histogram\n")
    rep = pdfreport.ReportWriter(output_file)
    rep.save_figure(plot_histogram(data, dset_name, bins, hist_range, sel_range))
    rep.close()

if __name__ == '__main__':
    main()
