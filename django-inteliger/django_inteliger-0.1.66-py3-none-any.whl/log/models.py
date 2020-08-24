from django.db import models
import core.models


class Log(core.models.Log):
    """
    :Nome da classe/função: Log
    :descrição: Classe abstrata de log de requisição
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    status_code = models.IntegerField(null=True)
    reason_phrase = models.CharField(max_length=500, null=True)
    metodo = models.CharField(max_length=30, null=True)
    ip = models.GenericIPAddressField(null=True)
    path = models.CharField(max_length=500, null=True)
    session_key = models.CharField(max_length=200, null=True)
    body = models.TextField(null=True)

    info_user = models.TextField(null=True)
    info_user_navegador_familia = models.CharField(max_length=200, null=True)
    info_user_navegador_versao = models.CharField(max_length=50, null=True)
    info_user_aparelho_familia = models.CharField(max_length=200, null=True)
    info_user_aparelho_modelo = models.CharField(max_length=200, null=True)
    info_user_os_familia = models.CharField(max_length=200, null=True)
    info_user_os_versao = models.CharField(max_length=50, null=True)

    info_user_is_bot = models.BooleanField(null=True)
    info_user_is_email_client = models.BooleanField(null=True)
    info_user_is_mobile = models.BooleanField(null=True)
    info_user_is_pc = models.BooleanField(null=True)
    info_user_is_tablet = models.BooleanField(null=True)
    info_user_is_touch_capable = models.BooleanField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class Query(core.models.Log):
    """
    :Nome da classe/função: Query
    :descrição: Classe abstrata de log de queries
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    time = models.FloatField(null=True)
    query = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class Erro(core.models.Log):
    """
    :Nome da classe/função: Erro
    :descrição: Classe abstrata de log de erros
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    erro = models.ForeignKey('core.Erro', on_delete=models.DO_NOTHING, null=True)
    tipo = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class Integracao(core.models.Log):
    """
    :Nome da classe/função: Integracao
    :descrição: Classe abstrata de log de integrações
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    servico = models.CharField(max_length=200, null=True)
    tipo = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=500, null=True)
    headers = models.TextField(null=True)
    body = models.TextField(null=True)
    status_code = models.IntegerField(null=True)
    response = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = True


class ClienteLog(Log):
    """
    :Nome da classe/função: ClienteLog
    :descrição: Classe de log de requisições do Cliente
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_log"'


class ClienteQuery(Query):
    """
    :Nome da classe/função: ClienteQuery
    :descrição: Classe de log de query do Cliente
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_query"'


class ClienteErro(Erro):
    """
    :Nome da classe/função: ClienteErro
    :descrição: Classe de log de erro do Cliente
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_erro"'


class ClienteIntegracao(Integracao):
    """
    :Nome da classe/função: ClienteIntegracao
    :descrição: Classe de log de integração do Cliente
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"cliente_integracao"'


class IndicadorLog(Log):
    """
    :Nome da classe/função: IndicadorLog
    :descrição: Classe de log de requisições do Indicador
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_log"'


class IndicadorQuery(Query):
    """
    :Nome da classe/função: IndicadorQuery
    :descrição: Classe de log de query do Indicador
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_query"'


class IndicadorErro(Erro):
    """
    :Nome da classe/função: IndicadorErro
    :descrição: Classe de log de erro do Indicador
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_erro"'


class IndicadorIntegracao(Integracao):
    """
    :Nome da classe/função: IndicadorIntegracao
    :descrição: Classe de log de integração do Indicador
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"indicador_integracao"'


class FornecedorLog(Log):
    """
    :Nome da classe/função: FornecedorLog
    :descrição: Classe de log de requisições do Fornecedor
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_log"'


class FornecedorQuery(Query):
    """
    :Nome da classe/função: FornecedorQuery
    :descrição: Classe de log de query do Fornecedor
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_query"'


class FornecedorErro(Erro):
    """
    :Nome da classe/função: FornecedorErro
    :descrição: Classe de log de erro do Fornecedor
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_erro"'


class FornecedorIntegracao(Integracao):
    """
    :Nome da classe/função: FornecedorIntegracao
    :descrição: Classe de log de integração do Fornecedor
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"fornecedor_integracao"'


class Venda_maisLog(Log):
    """
    :Nome da classe/função: Venda_maisLog
    :descrição: Classe de log de requisições do Venda Mais
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_log"'


class Venda_maisQuery(Query):
    """
    :Nome da classe/função: Venda_maisQuery
    :descrição: Classe de log de query do Venda Mais
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_query"'


class Venda_maisErro(Erro):
    """
    :Nome da classe/função: Venda_maisErro
    :descrição: Classe de log de erro do Venda Mais
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_erro"'


class Venda_maisIntegracao(Integracao):
    """
    :Nome da classe/função: Venda_maisIntegracao
    :descrição: Classe de log de integração do Venda Mais
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"venda_mais_integracao"'


class ProcessosLog(Log):
    """
    :Nome da classe/função: ProcessosLog
    :descrição: Classe de log de log do Processos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Log.Meta):
        abstract = False
        db_table = u'"log\".\"processos_log"'


class ProcessosQuery(Query):
    """
    :Nome da classe/função: ProcessosQuery
    :descrição: Classe de log de query do Processos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Query.Meta):
        abstract = False
        db_table = u'"log\".\"processos_query"'


class ProcessosErro(Erro):
    """
    :Nome da classe/função: ProcessosErro
    :descrição: Classe de log de erro do Processos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"processos_erro"'


class ProcessosIntegracao(Integracao):
    """
    :Nome da classe/função: ProcessosIntegracao
    :descrição: Classe de log de integração do Processos
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    class Meta(Erro.Meta):
        abstract = False
        db_table = u'"log\".\"processos_integracao"'
