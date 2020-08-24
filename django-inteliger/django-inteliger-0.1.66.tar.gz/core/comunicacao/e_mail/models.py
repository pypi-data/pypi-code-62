from django.db import models
import core.models
# Create your models here.


class EmailEndereco(core.models.Log):
    """
    :Nome da classe/função: EmailEndereco
    :descrição: Classe de endereços de e-mail
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    email = models.EmailField(max_length=200, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    host = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_email_endereco'

    def __str__(self):
        return self.email


class Email(core.models.Log):
    """
    :Nome da classe/função: Email
    :descrição: Classe de e-mail
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True, blank=True)
    assunto = models.CharField(max_length=200, null=True, blank=True)
    conteudo = models.TextField(null=True, blank=True)
    endereco = models.ForeignKey('EmailEndereco', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='endereco_email')
    variaveis = models.TextField(null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_email'

    def __str__(self):
        return self.nm_descritivo


class EmailLog(core.models.Log):
    """
    :Nome da classe/função: EmailLog
    :descrição: Classe de log de e-mail
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    email = models.ForeignKey('Email', on_delete=models.DO_NOTHING, null=True, blank=True)
    destinatario = models.CharField(max_length=200, null=True, blank=True)
    retorno = models.TextField(null=True, blank=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'comunicacao_email_log'
