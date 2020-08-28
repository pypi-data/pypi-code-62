# #encoding:utf-8
import smtplib
from .models import *


class InitialConfiguration(object):

    def __init__(self):
        self.errors = []

    def is_valid(self):
        from .config import configuration_registers, configuration_register_longs
        _is_valid = True

        # para validar que todos los registros existan
        for register in configuration_registers:
            if not Registry.objects.filter(nombre=register).exists():
                _is_valid = False
                self.errors.append('''Por favor prepara la aplicacion <a href="/mail/preparar_aplicacion/">click aqui</a>''')
        for register in configuration_register_longs:
            if not RegistryLong.objects.filter(nombre=register).exists():
                _is_valid = False
                self.errors.append('''Por favor prepara la aplicacion <a href="/mail/preparar_aplicacion/">click aqui</a>''')

        return _is_valid


class MicrosipMailServer(dict):
    ''' Objeto para enviar correos. '''

    def __init__(self, from_addr=None, smtp_host=None, smtp_port=None, smtp_username=None, smtp_password=None):
        self.from_addr = from_addr
        if not from_addr:
            self.from_addr = Registry.objects.get(nombre='Email').valor

        if not smtp_host:
            smtp_host = Registry.objects.get(nombre='SMTP_HOST').valor
        if not smtp_port:
            smtp_port = Registry.objects.get(nombre='SMTP_PORT').valor
        if not smtp_username:
            smtp_username = Registry.objects.get(nombre='SMTP_USERNAME').valor
        if not smtp_password:
            smtp_password = Registry.objects.get(nombre='SMTP_PASSWORD').valor

        if smtp_username and smtp_port and smtp_host and smtp_password:
            server = smtplib.SMTP(smtp_host, int(smtp_port))
            server.ehlo()
            try:
                server.starttls()
            except:
                pass
            server.login(str(smtp_username), str(smtp_password))

            self.smtpserver = server
        else:
            self.smtpserver = None

    def sendmail(self, destinatarios, asunto, mensaje, imagen, archivo):
        # Import the email modules
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage
        from email.mime.application import MIMEApplication

        msgp = MIMEMultipart('related')
        msgp['CCO'] = ','.join(destinatarios)
        msgp['From'] = self.from_addr
        msgp['Subject'] = asunto

        mensajet = MIMEText('%s %s'%(mensaje,'<br><br><br><img src="cid:image1">'), 'html', _charset="UTF-8")
        msgp.attach(mensajet)
        # IMAGEN
        if imagen:
            msgImage = MIMEImage(imagen.read(), _subtype="jpeg")
            msgImage.add_header('Content-ID', '<image1>')
            msgp.attach(msgImage)

        if archivo:
            msgpdf = MIMEApplication(archivo.read(), _subtype = 'pdf')
            msgp.add_header('Content-Disposition','',filename=archivo.name)
            msgp.attach(msgpdf)

        try:
            self.smtpserver.sendmail(self.from_addr, destinatarios, msgp.as_string())
        except smtplib.SMTPException:
            print ("Error: unable to send email")


# def sendmail(self, destinatarios, asunto, mensaje, imagen):
#         # Import the email modules
#         from email.mime.text import MIMEText
#         from email.mime.multipart import MIMEMultipart

#         msg = MIMEMultipart('alternative')
#         msg['CCO'] = ','.join(destinatarios)
#         msg['From'] = self.from_addr
#         msg['Subject'] = asunto
#         mensaje = MIMEText(mensaje, 'html', _charset="UTF-8")
#         msg.attach(mensaje)
#         try:
#             self.smtpserver.sendmail(self.from_addr, destinatarios, msg.as_string())
#         except smtplib.SMTPException:
#             print "Error: unable to send email"
