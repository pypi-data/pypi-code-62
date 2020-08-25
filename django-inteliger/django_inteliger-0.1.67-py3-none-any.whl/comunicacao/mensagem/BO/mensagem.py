import core.BO.integracao
import core.comunicacao.mensagem.models
import unicodedata


class Mensagem(core.BO.integracao.Integracao):
    """
    :Nome da classe/função: Email
    :descrição: Classe para envio de mensagem
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    def __init__(self, destinatario=None, request=None, modulo=None):
        url = None
        headers = None
        super(Mensagem, self).__init__(url=url, headers=headers, request=request, servico='nvoip', modulo=modulo)

        self.conteudo = None
        self.destinatario = destinatario
        self.mensagem = None

    def salvar_mensagem(self):
        """
        :Nome da classe/função: salvar_mensagem
        :descrição: Classe para salvar log de mensagem
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :status: Status de log
        """
        try:
            novo_log = core.comunicacao.mensagem.models.MensagemLog(
                mensagem_id=self.mensagem,
                destinatario=self.destinatario,
                retorno=self.response
            )
            novo_log.save()
            return True
        except:
            return False

    def enviar(self):
        """
         :Nome da classe/função: enviar
        :descrição: Classe para enviar mensagem
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return:  Status de envio
        """
        try:
            self.body = {
                "celular": ''.join(c for c in self.destinatario if c.isdigit()),
                "msg": unicodedata.normalize('NFD', self.conteudo[:160]).encode('ASCII', 'ignore').decode('utf-8')
            }
            self.post()
            self.salvar_mensagem()
            return True
        except:
            return False

    def carregar(self):
        """
        :Nome da classe/função: carregar
        :descrição: Classe para carregar a mensagem baseada no seu tipo
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return: Status de carregar
        """
        try:
            mensagem_info = core.comunicacao.mensagem.models.Mensagem.objects.ativos().filter(nome=self.mensagem).first()
            if mensagem_info is None:
                return False
            self.conteudo = mensagem_info.conteudo
            return True
        except:
            pass
        return False

    @property
    def conteudo(self):
        return self.__conteudo

    @conteudo.setter
    def conteudo(self, value):
        self.__conteudo = value

    @conteudo.deleter
    def conteudo(self):
        del self.__conteudo

    @property
    def destinatario(self):
        return self.__destinatario

    @destinatario.setter
    def destinatario(self, value):
        self.__destinatario = value

    @destinatario.deleter
    def destinatario(self):
        del self.__destinatario

    @property
    def mensagem(self):
        return self.__mensagem

    @mensagem.setter
    def mensagem(self, value):
        self.__mensagem = value

    @mensagem.deleter
    def mensagem(self):
        del self.__mensagem

