"""Simple calculator.

Implemeted as a Python expression evaluator.
"""

from math import *
import click

from . import cli


@cli.command()
@click.argument("expression")
def calc(expression):
    """Compute simple expressions."""

    print(eval(expression))
