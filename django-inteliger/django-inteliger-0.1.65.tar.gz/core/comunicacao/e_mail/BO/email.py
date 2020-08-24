import core.comunicacao.e_mail.models
import core.util.criptografia
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import core.comunicacao.e_mail.models
import core.comunicacao.mensagem.models


class Email:
    """
    :Nome da classe/função: Email
    :descrição: Classe para envio de e-mail
    :Criação: Nícolas Marinoni Grande - 17/08/2020
    :Edições:
    """
    def __init__(self, destinatario=None):
        self.email = None

        self.endereco = None
        self.password = None
        self.host = None
        self.port = None

        self.assunto = None
        self.conteudo = None

        self.destinatario = destinatario

        self.retorno = None

    def carregar(self):
        """
        :Nome da classe/função: carregar
        :descrição: Função que carrega o e-mail baseado no tipo
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return: Status de carregar
        """
        try:
            email_info = core.comunicacao.e_mail.models.Email.objects.ativos().filter(nome=self.email).first()
            if email_info is None:
                return False

            self.endereco = email_info.endereco.email
            self.password = self.descriptografar_senha(email_info.endereco.password)
            self.host = email_info.endereco.host
            self.port = email_info.endereco.port

            self.assunto = email_info.assunto
            self.conteudo = email_info.conteudo
            return True
        except:
            pass
        return False

    def criptografar_senha(self, senha):
        """
        :Nome da classe/função: criptografar_senha
        :descrição: Função para criptografar senha do email
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return: Token da senha criptografado
        """
        senha_token = core.util.criptografia.password_encrypt(message=senha, password='A3DF750D4245BA42B14EABCE7DDC3ACFDF4B9C30441DC3B8D8DF2C9A3D18FB6B')
        return senha_token.decode()

    def descriptografar_senha(self, senha_token):
        """
        :Nome da classe/função: descriptografar_senha
        :descrição: Função para descriptografar senha do email
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return: Senha descriptografada
        """
        senha = core.util.criptografia.password_decrypt(token=senha_token.encode(), password='A3DF750D4245BA42B14EABCE7DDC3ACFDF4B9C30441DC3B8D8DF2C9A3D18FB6B').decode()
        return senha

    def salvar_email(self):
        """
        :Nome da classe/função: salvar
        :descrição: Função para salvar log de envio de e-mail
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return: Status de log
        """
        try:
            novo_log = core.comunicacao.e_mail.models.EmailLog(
                email_id=self.email,
                destinatario=self.destinatario,
                retorno=self.retorno
            )
            novo_log.save()
            return True
        except:
            return False

    def enviar(self):
        """
        :Nome da classe/função: enviar
        :descrição: Função para enviar o e-mail
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :return: Status de envio
        """
        try:
            s = smtplib.SMTP(host=self.host, port=self.port)
            s.starttls()
            s.login(self.endereco, self.password)
            msg = MIMEMultipart()
            msg['From'] = self.endereco
            msg['To'] = self.destinatario
            msg['Subject'] = self.assunto
            msg.attach(MIMEText(self.conteudo, 'html'))
            self.retorno = s.send_message(msg)
            self.salvar_email()
            s.quit()
            return True
        except:
            return False

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @email.deleter
    def email(self):
        del self.__email

    @property
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, value):
        self.__endereco = value

    @endereco.deleter
    def endereco(self):
        del self.__endereco

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    @password.deleter
    def password(self):
        del self.__password

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @host.deleter
    def host(self):
        del self.__host

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @port.deleter
    def port(self):
        del self.__port

    @property
    def assunto(self):
        return self.__assunto

    @assunto.setter
    def assunto(self, value):
        self.__assunto = value

    @assunto.deleter
    def assunto(self):
        del self.__assunto

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
    def retorno(self):
        return self.__retorno

    @retorno.setter
    def retorno(self, value):
        self.__retorno = value

    @retorno.deleter
    def retorno(self):
        del self.__retorno
