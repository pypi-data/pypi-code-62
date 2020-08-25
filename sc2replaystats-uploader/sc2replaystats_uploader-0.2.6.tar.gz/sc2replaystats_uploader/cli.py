"""Console script for sc2replaystats_uploader."""
import sys
import click
from .sc2replaystats_uploader import run_watcher


@click.command()
@click.option(
    "--auth",
    required=True,
    help="sc2replaystats authorization key; find it in "
    "https://sc2replaystats.com/account/settings -> API Access",
    type=str,
    envvar="SC2REPLAYSTATS_AUTH",
)
@click.option(
    "--path",
    required=True,
    help="Directories in which to find replays. "
    "You can put multiple such options here."
    "If using multiple in an environment variable, "
    "separate them with a colon ':'.",
    multiple=True,
    type=click.Path(),
    envvar="SC2REPLAYSTATS_PATH",
)
def main(auth, path):
    """Console script for sc2replaystats_uploader."""
    run_watcher(auth, path)


if __name__ == "__main__":
    sys.exit(main(auto_envvar_prefix="SC2REPLAYSTATS"))  # pragma: no cover
