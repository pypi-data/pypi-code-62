import click

from fgbio_postprocessing import simplex_filter


@click.command()
@click.option("--input_bam", required=True, help="Path to bam to be filtered")
@click.option("--output_filename", required=True, help="Name of output bam")
@click.option("--min_simplex_reads", required=False, default=3, help="Minimum number of simplex reads to pass filter")
def calculate_noise(input_bam, output_filename, min_simplex_reads):
    """
    Filter bam file to only simplex reads with `min_simplex_reads` on one strand

    :param input_bam: string
    :param output_filename: string
    :param min_simplex_reads: int
    :return:
    """
    simplex_filter.main(input_bam, output_filename, min_simplex_reads)
    