"""Split a compressed text file into multiple smaller (compressed) text files."""

import gzip
import bz2
import lzma
from itertools import islice

import click
from tqdm import tqdm

from . import cli

COMP_OPEN = {"gzip": gzip.open, "bz2": bz2.open, "xz": lzma.open, "text": open}

COMP_OPTIONS = list(COMP_OPEN.keys()) + ["infer"]


def do_csplit(
    input_file,
    output_file_format,
    lines_per_file=1000,
    encoding="utf-8",
    input_compression="infer",
    output_compression="infer",
):
    """Split a large compressed text file into multiple smaller (compressed) text files.

    {index} in output_file_format will be replaced by index of the output file.
    index of output files start from 0
    """
    if input_compression == "infer":
        if input_file.endswith(".gz"):
            input_compression = "gzip"
        elif input_file.endswith(".bz2"):
            input_compression = "bz2"
        elif input_file.endswith(".xz"):
            input_compression = "xz"
        else:
            input_compression = "text"

    if output_compression == "infer":
        if output_file_format.endswith(".gz"):
            output_compression = "gzip"
        elif output_file_format.endswith(".bz2"):
            output_compression = "bz2"
        elif output_file_format.endswith(".xz"):
            output_compression = "xz"
        else:
            output_compression = "text"

    in_open = COMP_OPEN[input_compression]
    out_open = COMP_OPEN[output_compression]

    with in_open(input_file, mode="rt", encoding=encoding) as fin:
        fin = iter(fin)
        index = 0

        obar = tqdm(desc="Writing file")
        while True:
            lines = list(islice(fin, lines_per_file))
            if not lines:
                return

            ibar = tqdm(lines, desc="Writing line", leave=False)

            output_file = output_file_format.format(index=index)
            with out_open(output_file, mode="xt", encoding=encoding) as fout:
                for line in ibar:
                    fout.write(line)
            index += 1
            obar.update(1)

        obar.close()


@cli.command()
@click.option(
    "-n",
    "--lines-per-file",
    default=1000,
    help="Maximum number of lines per output file",
)
@click.option(
    "-e", "--encoding", default="utf-8", help="Text encoding of input and output files"
)
@click.option(
    "-c",
    "--input-compression",
    default="infer",
    type=click.Choice(COMP_OPTIONS),
    help="Compression format of the input file",
)
@click.option(
    "-d",
    "--output-compression",
    default="infer",
    type=click.Choice(COMP_OPTIONS),
    help="Compression format of output files",
)
@click.argument("input-file")
@click.argument("output-file-format")
def csplit(
    lines_per_file,
    encoding,
    input_compression,
    output_compression,
    input_file,
    output_file_format,
):
    """Split a large compressed text file into multiple smaller (compressed) text files.

    {index} in output_file_format will be replaced by index of the output file.
    index of output files start from 0
    """

    do_csplit(
        input_file,
        output_file_format,
        lines_per_file,
        encoding,
        input_compression,
        output_compression,
    )
