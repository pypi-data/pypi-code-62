from types import MethodType
from django.test.runner import DiscoverRunner
from django.db import connections


def prepare_database(self):
    """
    :Nome da classe/função: prepare_database
    :descrição: Função que conecta a uma database e executa o script para ser possível usar os tests do django
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    :param self: Conexão da database
    :return:
    """
    self.connect()
    self.connection.cursor().execute("""
    CREATE SCHEMA log;
    GRANT ALL ON SCHEMA log TO voai;
    GRANT ALL ON SCHEMA log TO cliente;
    """)


class PostgresSchemaTestRunner(DiscoverRunner):
    """
    :Nome da classe/função: PostgresSchemaTestRunner
    :descrição: Classe chamada na hora de gerar os tests do django e preparar a database
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    def setup_databases(self, **kwargs):
        """
        :Nome da classe/função: setup_databases
        :descrição: Função que constrói o database para tests
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :param kwargs:
        :return: Database construida
        """
        for connection_name in connections:
            connection = connections[connection_name]
            connection.prepare_database = MethodType(prepare_database, connection)
        return super().setup_databases(**kwargs)