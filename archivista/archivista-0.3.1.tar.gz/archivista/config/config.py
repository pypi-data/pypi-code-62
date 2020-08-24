import click
import configparser
from pathlib import Path
from archivista.universales.funciones import validar_rama


class Config(object):

    def __init__(self):
        self.rama = ''
        self.almacen_frio_url = ''
        self.descargables_extensiones = []
        self.fecha_por_defecto = ''
        self.imagenes_extensiones = []
        self.nextcloud_ruta = ''
        self.pelican_ruta = ''
        self.plantillas_ruta = ''
        self.plantilla = ''
        self.titulo = ''
        self.insumos_ruta = ''
        self.salida_ruta = ''

    def obtener_ramas(self):
        settings = configparser.ConfigParser()
        settings.read('settings.ini')
        return(settings.sections())

    def cargar_configuraciones(self, rama):
        """ Cargar configuraciones en settings.ini """
        if rama == '':
            raise Exception('ERROR: Faltó definir la rama.')
        self.rama = validar_rama(rama)
        settings = configparser.ConfigParser()
        settings.read('settings.ini')
        try:
            self.almacen_frio_url = settings['DEFAULT']['almacen_frio']
            self.descargables_extensiones = settings['DEFAULT']['descargables_extensiones'].split(',')
            self.fecha_por_defecto = settings['DEFAULT']['fecha_por_defecto']
            self.imagenes_extensiones = settings['DEFAULT']['imagenes_extensiones'].split(',')
            self.nextcloud_ruta = settings['DEFAULT']['nextcloud_ruta']
            self.pelican_ruta = settings['DEFAULT']['pelican_ruta']
            self.plantillas_ruta = settings['DEFAULT']['plantillas_ruta']
            self.plantilla = settings['DEFAULT']['plantilla']
            self.titulo = settings[self.rama]['titulo']
        except KeyError:
            raise Exception(f'ERROR: Falta configuración en settings.ini para la rama {self.rama}')
        # Validar la ruta de insumos desde Archivista
        self.insumos_ruta = Path(f'{self.nextcloud_ruta}/{self.titulo}')
        if not self.insumos_ruta.exists() or not self.insumos_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio de insumos {}'.format(str(self.insumos_ruta)))
        # Validar la ruta contents donde se crearán los archivos que usará Pelican
        self.salida_ruta = Path(f'{self.pelican_ruta}/content')
        if not self.salida_ruta.exists() or not self.salida_ruta.is_dir():
            raise Exception('ERROR: No existe el directorio de salida {}'.format(str(self.salida_ruta)))


pass_config = click.make_pass_decorator(Config, ensure=True)
