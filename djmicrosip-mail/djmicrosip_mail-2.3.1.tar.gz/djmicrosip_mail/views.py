#encoding:utf-8
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# user autentication
from .models import *
from .forms import *
import csv
from django.http import HttpResponse
from django.views.generic.list import ListView

from .core import InitialConfiguration
from .tasks import enviar_correo
from microsip_api.apps.cuentasxcobrar.core import CargosClientes


@login_required(login_url='/login/')
def envia_saldos_automaticos(request):
    enviar_remisiones = Registry.objects.get(nombre='SIC_MAIL_EnviarRemisionesPendientes').get_value() == 'S'
    monto_minimo_mn = Registry.objects.get(nombre='SIC_MAIL_MontoMinimo').get_value() or 0
    cargos = CargosClientes('email', tomar_remisiones=enviar_remisiones, monto_minimo_mn=monto_minimo_mn)

    mail_login = {
        'smtp_host': Registry.objects.get(nombre='SMTP_HOST').valor,
        'smtp_port': Registry.objects.get(nombre='SMTP_PORT').valor,
        'smtp_username': Registry.objects.get(nombre='SMTP_USERNAME').valor,
        'smtp_password': Registry.objects.get(nombre='SMTP_PASSWORD').valor,
        'from_addr': Registry.objects.get(nombre='Email').valor,
    }

    commun = {
        'empresa_nombre': Registry.objects.get(nombre='SIC_MAIL_EmpresaNombre').get_value(),
        'mensaje_extra': RegistryLong.objects.get(nombre='SIC_MAIL_MensajeExtra').valor,
    }

    kwargs = {
        'commun': commun,
        'mail_login': mail_login,
    }
    for cargo in cargos:
        kwargs['cargo'] = cargo
        enviar_correo(kwargs=kwargs)

    return HttpResponseRedirect('/mail/')


@login_required(login_url='/login/')
def index(request, template_name='djmicrosip_mail/index.html'):
    configuracion = InitialConfiguration()
    context = {}
    if not configuracion.is_valid():
        context['errors'] = configuracion.errors

    return render(request,template_name, context)
