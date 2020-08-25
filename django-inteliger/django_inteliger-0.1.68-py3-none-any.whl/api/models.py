from django.db import models
import core.usr.models
import core.models


# Create your models here.
class ApiLogin(core.usr.models.Profile):
    """
    :Nome da classe/função: ApiLogin
    :descrição: Classe de login para usuários de API
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """

    class Meta(core.models.Log.Meta):
        abstract = False
        db_table = 'api_login'
