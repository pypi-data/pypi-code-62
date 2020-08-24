from django.db import models
import core.models


# Create your models here.
class Fornecedor(core.models.Log):
    """
    :Nome da classe/função: Fornecedor
    :descrição: Classe de fornecedores
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'fornecedor'


class Fabricante(core.models.Log):
    """
    :Nome da classe/função: Fabricante
    :descrição: Classe de fabricantes
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    nome = models.CharField(max_length=200, null=True)

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'fabricante'
