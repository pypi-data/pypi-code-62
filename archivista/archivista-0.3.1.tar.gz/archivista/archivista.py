import click
import sys
from archivista.config.config import pass_config
from archivista.universales.rama import Rama


@click.group()
@pass_config
def cli(config):
    click.echo('Hola, ¡soy Archivista!')


@cli.command()
@pass_config
@click.option('--rama', default='', type=str, help='Directorio de insumos configurado en settings.ini')
def mostrar(config, rama):
    """ Mostrar lo que se encuentra en una rama """
    config.cargar_configuraciones(rama)
    rama = Rama(config)
    rama.alimentar()
    click.echo(repr(rama))
    sys.exit(0)


@cli.command()
@pass_config
def mostrar_todas(config):
    """ Mostrar lo que se encuentra en TODAS las ramas """
    for rama in config.obtener_ramas():
        config.cargar_configuraciones(rama)
        rama = Rama(config)
        rama.alimentar()
        click.echo(repr(rama))
    sys.exit(0)


@cli.command()
@pass_config
@click.option('--rama', default='', type=str, help='Directorio de insumos configurado en settings.ini')
def crear(config, rama):
    """ Crear una rama """
    config.cargar_configuraciones(rama)
    rama = Rama(config)
    rama.alimentar()
    click.echo(rama.crear())
    sys.exit(0)


@cli.command()
@pass_config
def crear_todas(config):
    """ Crear TODAS las ramas """
    for rama in config.obtener_ramas():
        config.cargar_configuraciones(rama)
        rama = Rama(config)
        rama.alimentar()
        click.echo(rama.crear())
    sys.exit(0)


cli.add_command(mostrar)
cli.add_command(mostrar_todas)
cli.add_command(crear)
cli.add_command(crear_todas)
