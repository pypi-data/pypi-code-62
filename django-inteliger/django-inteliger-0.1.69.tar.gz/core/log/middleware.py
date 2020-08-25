from core.views import Inteliger


class LogMiddleware:
    """
    :Nome da classe/função: LogMiddleware
    :descrição: Classe de Middleware para salvar log de requisições
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """

    def __init__(self, get_response):
        """
        :Nome da classe/função: __init__
        :descrição: Define a resposta ao inicializar a classe
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :param get_response: Resposta
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        :Nome da classe/função: __call__
        :descrição: Salva o log ao chamar a classe
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :param request:
        :return:
        """
        response = self.get_response(request)
        Inteliger().salvar_log(request=request, response=response)
        return response
