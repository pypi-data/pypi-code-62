"""Hello world command."""

from click import secho
from . import cli

@cli.command()
def hello():
    """Print "Hello, world!"."""
    secho("Hello, world!", fg="green")
