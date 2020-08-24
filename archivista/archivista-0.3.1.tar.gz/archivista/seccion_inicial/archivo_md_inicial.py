from pathlib import Path


class ArchivoMdInicial(object):
    """ Archivo md inicial """

    def __init__(self, config, ruta, nivel):
        self.config = config
        if isinstance(ruta, str):
            self.ruta = Path(ruta)
        else:
            self.ruta = ruta
        self.nivel = nivel
        self.ya_alimentado = False
        self.archivo_md_nombre = None
        self.archivo_md_ruta = None

    def alimentar(self):
        """ Alimentar """
        if self.ya_alimentado is False:
            # La ruta puede ser un directorio o el archivo md
            if self.ruta.exists() and self.ruta.is_dir():
                # La ruta es un directorio
                posible_nombre = self.ruta.parts[-1] + '.md'
                posible_ruta = Path(self.ruta, posible_nombre)
                if posible_ruta.exists() and posible_ruta.is_file():
                    self.archivo_md_nombre = posible_nombre
                    self.archivo_md_ruta = posible_ruta
            elif self.ruta.exists() and self.ruta.is_file():
                # La ruta es un archivo
                self.archivo_md_nombre = posible_nombre
                self.archivo_md_ruta = posible_ruta
            # Levantar bandera
            self.ya_alimentado = True
        # Entregar verdadero si hay
        return(self.archivo_md_ruta is not None)

    def contenido(self):
        """ Contenido entrega texto markdown """
        if self.ya_alimentado and self.archivo_md_ruta is not None:
            with open(str(self.archivo_md_ruta), 'r') as puntero:
                return(puntero.read())
        else:
            return('')

    def __repr__(self):
        return('  ' * self.nivel + f'<ArchivoMdInicial> {self.archivo_md_nombre}')
