"""Convert between 1S08601 UTC and Unix timestamp."""

from datetime import datetime, timezone

import click
from dateutil.parser import isoparse

from . import cli


@cli.command()
@click.argument("time")
def timefmt(time):
    """Convert between UTC ISO8601 datetime string and Unix timestamp."""
    if time == "now":
        time = datetime.now()
    else:
        try:
            time = float(time)
            time = datetime.utcfromtimestamp(time)
        except ValueError:
            time = isoparse(time)

    if time.tzinfo is None:
        time = time.replace(tzinfo=timezone.utc)

    click.secho("Date: %s" % time.isoformat(), fg="green")
    click.secho("Timestamp: %s" % time.timestamp(), fg="yellow")
