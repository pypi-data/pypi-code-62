from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models


# Create your models here.
class Modulo(core.models.Log):
    """
    :Nome da classe/função: Modulo
    :descrição: Classe de modulos de sistema
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.SlugField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    modulo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_modulo'


class Versao(core.models.Log):
    """
    :Nome da classe/função: Modulo
    :descrição: Classe de versões do código para módulo
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    modulo = models.ForeignKey('sistema.Modulo', null=True, on_delete=models.DO_NOTHING)
    dat_atualizacao = models.DateField(null=True)
    codigo = models.CharField(max_length=100, null=True)
    commit = models.CharField(max_length=50, null=True)
    descricao = models.TextField(null=True)

    responsavel_id = models.IntegerField(null=True)
    responsavel_codigo = models.CharField(null=True, max_length=200)
    responsavel_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    responsavel = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_responsavel', to_fields={
        "codigo": "responsavel_codigo",
        "tipo": "responsavel_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_versao'


class VersaoItem(core.models.Log):
    """
    :Nome da classe/função: VersaoItem
    :descrição: Classe de itens das versões
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    versao = models.ForeignKey('sistema.Versao', null=True, on_delete=models.DO_NOTHING)
    ordem = models.IntegerField(null=True)
    descricao = models.TextField(null=True)

    responsavel_id = models.IntegerField(null=True)
    responsavel_codigo = models.CharField(null=True, max_length=200)
    responsavel_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    responsavel = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_responsavel', to_fields={
        "codigo": "responsavel_codigo",
        "tipo": "responsavel_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_versaoitem'


class PontoFuncao(core.models.Log):
    """
    :Nome da classe/função: PontoFuncao
    :descrição: Classe de pontos de função do sistema
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    modulo = models.ForeignKey('sistema.Modulo', null=True, on_delete=models.DO_NOTHING)
    acao = models.CharField(max_length=100, primary_key=True)
    codigo = models.IntegerField(null=True)

    versao = models.CharField(max_length=10, null=True)
    descricao = models.CharField(max_length=500, null=True)

    lugares = models.TextField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_pontofuncao'


class Perfil(core.models.Log):
    """
    :Nome da classe/função: Perfil
    :descrição: Classe de perfil de acesso ao sistema que se relaciona com grupos de usuários e pontos de função
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nivel = models.IntegerField(null=True)
    is_login = models.BooleanField(null=True)
    is_staff = models.BooleanField(default=False)
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    descricao = models.CharField(max_length=500, null=True)
    pontofuncao = models.ManyToManyField('sistema.PontoFuncao', through='sistema.PerfilPontoFuncao', through_fields=('perfil', 'pontofuncao'))
    perfil_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_perfil'


class PerfilPontoFuncao(core.models.Log):
    """
    :Nome da classe/função: PerfilPontoFuncao
    :descrição: Classe de relação entre Perfil e Ponto Função
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    pontofuncao = models.ForeignKey('sistema.PontoFuncao', on_delete=models.DO_NOTHING, null=True)
    perfil = models.ForeignKey('sistema.Perfil', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_perfilpontofuncao'


class PerfilLogin(core.models.Log):
    """
    :Nome da classe/função: PerfilLogin
    :descrição: Classe de relação entre o perfil, o módulo e qual a view inicial nesse sistema do usuário
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    modulo = models.ForeignKey('sistema.Modulo', null=True, on_delete=models.DO_NOTHING)
    perfil = models.ForeignKey('sistema.Perfil', on_delete=models.DO_NOTHING)
    view_inicial = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_perfillogin'


class PerfilUsr(core.models.Log):
    """
    :Nome da classe/função: PerfilGrupo
    :descrição: Classe de relação entre o perfil no sistema e grupo de usuário
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    perfil = models.ForeignKey('sistema.Perfil', on_delete=models.DO_NOTHING, null=True)
    dat_ini = models.DateField(null=True)
    dat_fim = models.DateField(null=True)

    usr_id = models.IntegerField(null=True)
    usr_codigo = models.CharField(null=True, max_length=200)
    usr_tipo = models.CharField(null=True, max_length=200, default='USR.PROFILE')
    usr = CompositeForeignKey('core.Tipo', on_delete=models.DO_NOTHING, null=True, related_name='%(app_label)s_%(class)s_usr', to_fields={
        "codigo": "usr_codigo",
        "tipo": "usr_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'sistema_perfilusr'
