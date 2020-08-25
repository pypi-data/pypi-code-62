from django.db import models
import core.models


# Create your models here.
class Mensagem(core.models.Log):
    """
    :Nome da classe/função: Mensagem
    :descrição: Classe de tipos de mensagens
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True, blank=True)
    conteudo = models.TextField(null=True, blank=True)
    variaveis = models.TextField(null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_mensagem'

    def __str__(self):
        return self.nm_descritivo


class MensagemLog(core.models.Log):
    """
    :Nome da classe/função: MensagemLog
    :descrição: Classe de log de mensagens
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    mensagem = models.ForeignKey('Mensagem', on_delete=models.DO_NOTHING, null=True, blank=True)
    destinatario = models.CharField(max_length=200, null=True, blank=True)
    retorno = models.TextField(null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_mensagem_log'
