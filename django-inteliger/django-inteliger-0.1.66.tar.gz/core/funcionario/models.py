from django.db import models
import core.models
import core.usr.models
# Create your models here.


class FuncionarioLogin(core.usr.models.Profile):
    """
    :Nome da classe/função: FuncionarioLogin
    :descrição: Classe de login para funcionários
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    funcionario = models.OneToOneField('funcionario.Funcionario', on_delete=models.DO_NOTHING, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'funcionario_login'


class Funcionario(core.models.Log, core.models.PessoaLog):
    """
    :Nome da classe/função: FuncionarioLogin
    :descrição: Classe de funcionários e informações pessoais
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    matricula = models.CharField(max_length=200, primary_key=True)
    cargo = models.ForeignKey('funcionario.Cargo', on_delete=models.DO_NOTHING, null=True)
    imagem = models.FileField(upload_to='fotos/funcionarios', default='fotos/sem-foto.png', null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'funcionario'


class Cargo(core.models.Log):
    """
    :Nome da classe/função: FuncionarioLogin
    :descrição: Classe de cargos de funcionários
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, primary_key=True)
    cargo_pai = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)
    nm_descritivo = models.CharField(max_length=500, null=True)
    funcao = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'cargo'
