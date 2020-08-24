from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class ForgivingManifestStaticFilesStorage(ManifestStaticFilesStorage):
    """
    :Nome da classe/função: ForgivingManifestStaticFilesStorage
    :descrição: Classe feita para atualizar os arquivos com hash para não gerar cache no collectstatic
    :Criação: Juan Sanguino - 17/08/2020
    :Edições:
    """
    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        """
        :Nome da classe/função: hashed_name
        :descrição: Função da classe que gera os hashs para salvar os arquivos
        :Criação: Juan Sanguino - 17/08/2020
        :Edições:
        :param name: Nome base para construir a hash
        :param content: Conteúdo do arquivo
        :param filename: Nome do arquivo
        :return: Arquivo processado
        """
        try:
            result = super().hashed_name(name, content, filename)
        except ValueError:
            # When the fille is missing, let's forgive and ignore that.
            result = name
        return result
