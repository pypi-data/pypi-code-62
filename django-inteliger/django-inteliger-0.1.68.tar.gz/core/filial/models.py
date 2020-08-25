from compositefk.fields import CompositeForeignKey
from django.db import models
import core.models
# Create your models here.


class Filial(core.models.Log, core.models.EmpresaLog, core.models.EnderecoComplementoLog, core.models.ContatoLog):
    """
    :Nome da classe/função: Filial
    :descrição: Classe de filiais e suas informações principais
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    --- 18/08/2020 - Nícolas Marinoni Grande
    - Motivo: Inserção dos campos ip_acesso, area, areas, dat_abertura, dat_fechamento, is_loja, e hierarquia da tabela de ContatoLog. Remoção do campo telefone.

    """
    cd_filial = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nome_completo = models.CharField(max_length=200, null=True)
    cnpj = models.CharField(max_length=50, null=True)

    ip_acesso = models.CharField(max_length=100, null=True)
    area = models.ForeignKey('filial.Area', on_delete=models.DO_NOTHING, null=True, related_name='area_atual')

    servicos = models.ManyToManyField('filial.Servico', through='FilialServico', through_fields=('cd_filial', 'servico'))

    dat_abertura = models.DateField(null=True)
    dat_fechamento = models.DateField(null=True)
    is_loja = models.BooleanField(null=True, default=True)

    areas = models.ManyToManyField('filial.Area', through='FilialArea', through_fields=('cd_filial', 'area'))

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial'

    def __str__(self):
        return self.nome


class Area(core.models.Log):
    """
    :Nome da classe/função: Area
    :descrição: Classe de áreas genéricas da filial
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    cd_area = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=200, null=True)
    nome_completo = models.CharField(max_length=200, null=True)
    responsavel = models.ForeignKey('funcionario.Funcionario', on_delete=models.DO_NOTHING, null=True)
    area_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='FILIAL.AREA')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='filial_area', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_area'

    def __str__(self):
        return self.nome


class FilialArea(core.models.Log):
    """
    :Nome da classe/função: FilialArea
    :descrição: Classe de relação história entre filial e área
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    area = models.ForeignKey('filial.Area', on_delete=models.DO_NOTHING, null=True)
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True)
    responsavel = models.ForeignKey('funcionario.Funcionario', on_delete=models.DO_NOTHING, null=True)

    dat_ini = models.DateField(null=True)
    dat_fim = models.DateField(null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_filialarea'


class Servico(core.models.Log):
    """
    :Nome da classe/função: Servico
    :descrição: Classe de serviços possíveis que uma filial pode ofertar
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
     --- 18/08/2020 - Nícolas Marinoni Grande
    - Motivo: Alteração do campo Id para nome
    """
    nome = models.CharField(max_length=200, primary_key=True)
    nm_descritivo = models.CharField(max_length=200, null=True)
    descricao = models.TextField(null=True)

    tipo_codigo = models.CharField(null=True, max_length=200)
    tipo_tipo = models.CharField(null=True, max_length=200, default='FILIAL.SERVICO')
    tipo = CompositeForeignKey(core.models.Tipo, on_delete=models.DO_NOTHING, null=True, related_name='filial_servico_tipo', to_fields={
        "codigo": "tipo_codigo",
        "tipo": "tipo_tipo"
    })

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_servico'

    def __str__(self):
        return self.nome


class FilialServico(core.models.Log):
    """
    :Nome da classe/função: FilialServico
    :descrição: Classe de relação de filial com serviços
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    --- 18/08/2020 - Nícolas Marinoni Grande
    - Motivo: Inserção do campo informacoes
    """
    servico = models.ForeignKey('filial.Servico', on_delete=models.DO_NOTHING, null=True)
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True)

    informacao = models.CharField(max_length=500, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_filialservico'


class FilialHoraFuncionamento(core.models.Log):
    """
    :Nome da classe/função: FilialHoraFuncionamento
    :descrição: Classe de relação de filial com o seu horário de funcionamento
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    is_padrao = models.BooleanField(null=True, default=True)
    dat_ini_validade = models.DateField(null=True)
    dat_fim_validade = models.DateTimeField(null=True)

    cd_hr_util_inicio = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_util_inicio")
    cd_hr_util_fim = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_util_fim")
    cd_hr_sab_inicio = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_sab_inicio")
    cd_hr_sab_fim = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_sab_fim")
    cd_hr_dom_inicio = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_dom_inicio")
    cd_hr_dom_fim = models.ForeignKey('core.Hora', null=True, on_delete=models.DO_NOTHING, related_name="cd_hr_dom_fim")
    cd_filial = models.ForeignKey('filial.Filial', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'filial_horafuncionamento'
