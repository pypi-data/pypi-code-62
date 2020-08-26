from django.http import JsonResponse
from django.views import View

from core.util.core import Inteliger


class InteligerView(View):
    """
    :Nome da classe/função: InteligerView
    :descrição: View feita para atualizar o singleton de sistema
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    def get(self, request, *args, **kwargs):
        """
        :Nome da classe/função: get
        :descrição: Função get que é chamada quando é feita uma requisição do tipo GET na View
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :param request: informações da requisição
        :param args:
        :param kwargs:
        :return: Json com status de sucesso
        """
        Inteliger().atualizar_tempo_query()
        return JsonResponse({'status': 'Sistema atualizado com sucesso!'}, safe=False)
