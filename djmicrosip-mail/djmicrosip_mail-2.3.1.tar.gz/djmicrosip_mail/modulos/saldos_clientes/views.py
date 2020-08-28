#encoding:utf-8
from microsip_api.comun.sic_db import first_or_none
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# user autentication
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.conf import settings
from ...tasks import enviar_correo
from .core import formar_correo_por_vencer
from microsip_api.apps.cuentasxcobrar.core import CargosClientes
import csv
from datetime import date,datetime


@login_required(login_url='/login/')
def PorSeleccionView(request, template_name='djmicrosip_mail/saldos_clientes/por_seleccion.html'):
    form = SelectMultipleClients(request.POST or None)
    c = {'form': form}
    return render(request,template_name, c)


@login_required(login_url='/login/')
def mensajes_masivos(request, template_name='djmicrosip_mail/saldos_clientes/todos.html'):

    return render(request,template_name, {})


@login_required(login_url='/login/')
def enviar_cargos_seleccion(request):
    cargo = json.loads(request.GET['data'])
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
        'cargo': cargo,
    }

    enviar_correo(kwargs=kwargs)
    resultado = 'Mensaje enviado'

    data = json.dumps({
        'resultado': resultado,
        'destinatarios':cargo['email'].split(';'),
    })
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='/login/')
def enviar_cargos_por_vencer(request,  template_name='djmicrosip_mail/saldos_clientes/por_vencer.html'):
    # ids = [3638,]
    ids = []
    enviar_remisiones = Registry.objects.get(nombre='SIC_MAIL_EnviarRemisionesPendientes').get_value() == 'S'
    monto_minimo_mn = Registry.objects.get(nombre='SIC_MAIL_MontoMinimo').get_value() or 0
    cargos = CargosClientes('email', tomar_remisiones=enviar_remisiones, clientes_ids=ids, monto_minimo_mn=monto_minimo_mn)
    clientes_email_invalido = cargos.clientes_informacion_invalida
    clientes_sin_mensaje = cargos.clientes_sin_mensaje
    clientes_sin_mensaje = map(str, clientes_sin_mensaje)

    data = {
        'cargos': cargos,
        'clientes_email_invalido': clientes_email_invalido,
        'clientes_sin_mensaje': clientes_sin_mensaje,
    }

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
        'data': data,
    }

    formar_correo_por_vencer(kwargs=kwargs)
    resultado = 'Mensaje enviado'

    data = {
        'resultado': resultado,
    }
    return render(request,template_name, data)

def crear_archivo(request):
    destinatarios =json.loads(request.GET['destinatarios'])
    today=date.today()
    filename=str(today.day)+'-'+str(today.month)+'-'+str(today.year)+'.csv'
    with open(filename ,'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter=',')
        wr.writerow("Email enviados")
        for des in destinatarios:
            insert=des
            wr.writerow(insert)
    return HttpResponse("Listo", content_type='application/json')

@login_required(login_url='/login/')
def get_mensajes_saldos(request):
    ids = json.loads(request.GET['data'])
    # debugger
    enviar_remisiones = Registry.objects.get(nombre='SIC_MAIL_EnviarRemisionesPendientes').get_value() == 'S'
    monto_minimo_mn = Registry.objects.get(nombre='SIC_MAIL_MontoMinimo').get_value() or 0
    cargos = CargosClientes('email', tomar_remisiones=enviar_remisiones, clientes_ids=ids, monto_minimo_mn=monto_minimo_mn)
    clientes_email_invalido = cargos.clientes_informacion_invalida
    clientes_sin_mensaje = cargos.clientes_sin_mensaje
    clientes_sin_mensaje = str(clientes_sin_mensaje)
    print("-----------------------")
    print(clientes_sin_mensaje)
    print("-----------------------")
    # debugger
    data = json.dumps({
        'cargos': cargos,
        'clientes_email_invalido': clientes_email_invalido,
        'clientes_sin_mensaje': clientes_sin_mensaje,
    })
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='/login/')
def saldos_automaticos_preferencias(request, template_name='djmicrosip_mail/saldos_clientes/saldos_automaticos_preferencias.html'):
    context = {
        'errors': []
    }
    if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
        from djmicrosip_tareas.models import ProgrammedTask
        task = first_or_none(ProgrammedTask.objects.filter(description='Mail Saldos Automaticos')) or ProgrammedTask()

        form = ProgrammedTaskForm(request.POST or None, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.id:
                task.description = 'Mail Saldos Automaticos'
                task.command_type = 'http'
                task.command = 'http://127.0.0.1:8001/mail/saldos/todos_automatico/'
            task.save()
            form = ProgrammedTaskForm(None, instance=task)
        context['form'] = form
    else:
        context['errors'].append('Por favor instalarla para poder configurar esta opción')

    return render(request,template_name, context)

@login_required(login_url='/login/')
def saldos_por_vencer_automaticos_preferencias(request, template_name='djmicrosip_mail/saldos_clientes/saldos_automaticos_por_vencer_preferencias.html'):
    context = {
        'errors': []
    }
    if 'djmicrosip_tareas' in settings.EXTRA_MODULES:
        from djmicrosip_tareas.models import ProgrammedTask
        task = first_or_none(ProgrammedTask.objects.filter(description='Mail Saldos por vencer Automaticos')) or ProgrammedTask()

        form = ProgrammedTaskForm(request.POST or None, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.id:
                task.description = 'Mail Saldos por vencer Automaticos'
                task.command_type = 'http'
                task.command = 'http://127.0.0.1:8001/mail/saldos/enviar_por_vencer/'
            task.save()
            form = ProgrammedTaskForm(None, instance=task)
        context['form'] = form
    else:
        context['errors'].append('Por favor instalarla para poder configurar esta opción')

    return render(request,template_name, context)