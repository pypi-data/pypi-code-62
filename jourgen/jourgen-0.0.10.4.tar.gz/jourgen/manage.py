import click
import os
from livereload import Server
from jourgen.jourgen import (build_site, SITE_DIR, PAGES_DIR, TEMPLATES_DIR,
                             POSTS_DIR, STATIC_DIR)
from settings import common_template_variables, templateEnv


@click.group()
def cli():
    pass


def _build():
    common_template_variables['site_url'] = ""
    build_site(templateEnv, common_template_variables)


@cli.command()
@click.argument('host', required=False)
@click.argument('port', required=False)
def serve(host, port):
    """Start a live server for developing your journal in real time

    PORT defaults to 5500
    HOST defaults to 127.0.0.1
    """

    _build()

    if port is None:
        port = 5500

    if host is None:
        host = "127.0.0.1"

    server = Server()
    server.watch(os.path.join(SITE_DIR,  '**'))
    server.watch(os.path.join(TEMPLATES_DIR, '**'), _build)
    server.watch(os.path.join(PAGES_DIR, '**'), _build)
    server.watch(os.path.join(POSTS_DIR, '**'), _build)
    server.watch(os.path.join(STATIC_DIR, '**'), _build)

    server.serve(root='site', host=host, port=port)


@cli.command()
def build():
    build_site(templateEnv, common_template_variables)


if __name__ == "__main__":
    cli()
