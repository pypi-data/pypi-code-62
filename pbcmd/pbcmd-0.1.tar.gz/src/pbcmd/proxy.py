"""Start a ssh based socks proxy using autossh."""

import click
from subprocess import run

from . import cli

@cli.command()
@click.option("-p", "--port", default=12001, help="Local port to listen on")
@click.argument("host", type=str, nargs=1)
def proxy(port, host):
    """Start a ssh proxy on local port to remove host."""
    click.secho(f"Starting proxy to {host} on port {port}", fg="green")

    cmd = [
        "autossh",
        "-M", "0",
        "-o", "ServerAliveInterval 10",
        "-o", "ServerAliveCountMax 3",
        "-o", "ExitOnForwardFailure=yes",
        "-v",
        "-N",
        "-S", "none",
        "-D", f"127.0.0.1:{port}",
        host
    ]
    run(cmd, check=True)
