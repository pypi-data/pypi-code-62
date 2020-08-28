"""Simple Graph Generator"""

import argparse
from itertools import zip_longest
from math import log10
import importlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sgg.ext


def read_file(filename):
    """ 'filename' should be a two column file. This
        function will return, as two lists, the first and second column of this file.
    """
    x, y = [], []
    with open(filename, "r") as f:
        for l in f:
            if l[0] != "#":
                l = l.split()
                x.append(float(l[0]))
                y.append(float(l[1]))

        return x, y


def main():
    """Our main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", type=str, help="The graphs' title.")
    parser.add_argument("--xmin", type=float, help="The min value for the X axis.")
    parser.add_argument("--ymin", type=float, help="The min value for the Y axis.")
    parser.add_argument("--xmax", type=float, help="The max value for the X axis.")
    parser.add_argument("--ymax", type=float, help="The max value for the Y axis.")
    parser.add_argument(
        "--xlabel",
        "-x",
        type=str,
        help="The X label of the graph.",
        default=r"\textit{k}",
    )
    parser.add_argument(
        "--ylabel", "-y", type=str, help="The Y label of the graph.", default=""
    )
    parser.add_argument(
        "--styles",
        "-s",
        nargs="+",
        type=str,
        help="The style of each line in the graph.",
        default=[],
    )
    parser.add_argument(
        "--labels",
        "-l",
        nargs="+",
        type=str,
        help="The labels of the files.",
        default=[],
    )
    parser.add_argument(
        "--colors",
        "-c",
        nargs="+",
        type=str,
        help="The colors of the graphs.",
        default=[],
    )
    parser.add_argument(
        "--files",
        "-f",
        nargs="+",
        type=str,
        help="The files to be plotted.",
        required=True,
    )
    parser.add_argument(
        "--eps-file",
        "-e",
        type=str,
        help="Save the eps version of the image to the file passed to this option.",
    )

    parser.add_argument(
        "--ps-file",
        "-p",
        type=str,
        help="Save the ps version of the image to the file passed to this option.",
    )

    parser.add_argument(
        "--dest", "-d", type=str, help="File to which print the png image.",
    )

    parser.add_argument(
        "--yt", type=str, help="Transformation to apply to the Y axis. Default is none."
    )

    parser.add_argument(
        "--ext-file", type=str, help="The extension file to use. If not provided, use the builtin."
    )

    args = parser.parse_args()

    plt.rc("text", usetex=True)
    plt.rc("text.latex", preamble=r"\usepackage{amsmath}")
    plt.rc("font", family="serif")

    plt.grid(True)

    plt.xlabel(args.xlabel, fontsize=20)
    plt.ylabel(args.ylabel, fontsize=20)

    if args.title:
        plt.title(args.title)

    if args.xmin:
        plt.xlim(left=args.xmin)

    if args.xmax:
        plt.xlim(right=args.xmax)

    if args.ymin:
        plt.ylim(bottom=args.ymin)

    if args.ymax:
        plt.ylim(top=args.ymax)

    handles = []
    for filename, label, color, style in zip_longest(args.files,
                                                     args.labels,
                                                     args.colors,
                                                     args.styles):
        if filename is None:
            break

        x, y = read_file(filename)
        if args.yt:
            mod = sgg.ext
            if args.ext_file:
                spec = importlib.util.spec_from_file_location("module.name", args.ext_file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

            yt = mod.__dict__[args.yt]
            y = [yt(val) for val in y]

        if style is None:
            style = "-"
        else:
            style = style.lstrip()

        (l,) = plt.plot(x, y, linewidth=4, linestyle=style, label=label, color=color)
        handles.append(l)

    plt.legend(handles=handles, fontsize=16)
    plt.tick_params(labelsize=16)
    plt.tight_layout()

    if args.eps_file:
        plt.savefig(args.eps_file, format="eps")

    if args.ps_file:
        plt.savefig(args.ps_file, format="ps")

    if args.dest:
        plt.savefig(args.dest)


if __name__ == "__main__":
    main()
