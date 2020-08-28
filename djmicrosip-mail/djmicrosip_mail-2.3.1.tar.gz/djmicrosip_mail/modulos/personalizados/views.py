#encoding:utf-8
# user autentication
from ...core import MicrosipMailServer
from .core import *
from .forms import *
from .models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,render
from django.template import RequestContext
import xlrd
modo_pruebas = settings.MODO_SERVIDOR == 'PRUEBAS'


def get_num_enviados(respuestas):
    num_enviados = 0
    if type(respuestas) == list:
        num_enviados = 0
        for m in respuestas:
            if m['estatus'] == 'ok':
                num_enviados += 1
    return num_enviados


@login_required(login_url='/login/')
def PorSeleccionView(request, template_name='djmicrosip_mail/personalizados/por_seleccion.html'):
    form = SelectMultipleClients(request.POST or None, request.FILES)
    message = ''
    if form.is_valid():
        imagen = form.cleaned_data['imagen']
        archivo = form.cleaned_data['archivo']
        clientes = form.cleaned_data['clientes']
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']
        destinatarios = ClienteDireccion.objects.exclude(email=None).filter(cliente__in=clientes, es_ppal='S').values_list('email', flat=True)
        server = MicrosipMailServer()
        server.sendmail(destinatarios, asunto, mensaje,imagen, archivo)
        message = 'Correos envíados correctamente :D'
    c = {'mensaje': message, 'form': form, 'estatus': 'ok', }

    return render(request,template_name, c)


@login_required(login_url='/login/')
def todos_view(request, template_name='djmicrosip_mail/personalizados/todos.html'):
    form = MailAllForm(request.POST or None, request.FILES)
    message = ''
    if form.is_valid():
        imagen = form.cleaned_data['imagen']
        archivo = form.cleaned_data['archivo']
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']
        destinatarios = ClienteDireccion.objects.exclude(email=None).filter(es_ppal='S').values_list('email', flat=True)
        server = MicrosipMailServer()
        server.sendmail(destinatarios, asunto, mensaje,imagen, archivo)
        message = 'Correos envíados correctamente :D'
    c = {'mensaje': message, 'form': form, 'estatus': 'ok', }

    return render(request,template_name, c)


@login_required(login_url='/login/')
def zona_view(request, template_name='djmicrosip_mail/personalizados/zona.html'):
    form = ZonaForm(request.POST or None, request.FILES)
    message = ''
    if form.is_valid():        
        imagen = form.cleaned_data['imagen']
        archivo = form.cleaned_data['archivo']
        zona = form.cleaned_data['zona']
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']
        destinatarios = ClienteDireccion.objects.exclude(email=None).filter(cliente__zona=zona, es_ppal='S').values_list('email', flat=True)
        server = MicrosipMailServer()
        server.sendmail(destinatarios, asunto, mensaje,imagen, archivo)
        message = 'Correos envíados correctamente :D'
    c = {'mensaje': message, 'form': form, 'estatus': 'ok', }
    return render(request,template_name, c)


@login_required(login_url='/login/')
def abierto_view(request, template_name='djmicrosip_mail/personalizados/abierto.html'):
    form = MailForm(request.POST or None, request.FILES)
    message = ''
    if form.is_valid():
        imagen = form.cleaned_data['imagen']
        archivo = form.cleaned_data['archivo']
        destinatarios = form.cleaned_data['destinatario'].split(',')
        mensaje = form.cleaned_data['mensaje']
        asunto = form.cleaned_data['asunto']
        server = MicrosipMailServer()
        server.sendmail(destinatarios, asunto, mensaje, imagen, archivo)
        message = 'Correo envíado correctamente :D'
    context = {
        'form': form,
        'message': message,
    }
    return render(request,template_name, context)


@login_required(login_url='/login/')
def archivo_view(request, template_name='djmicrosip_mail/personalizados/archivo.html'):
    form = MailFileForm(request.POST or None, request.FILES or None)
    message = ''
    destinatarios_list = []
    if form.is_valid():
        asunto = form.cleaned_data['asunto']
        mensaje = form.cleaned_data['mensaje']
        destinatarios = form.cleaned_data['archivo']
        book = xlrd.open_workbook(file_contents=destinatarios.read())
        sheet = book.sheet_by_index(0)
        num_rows = sheet.nrows - 1
        num_cells = sheet.ncols - 1
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            curr_cell = -1
            while curr_cell < num_cells:
                curr_cell += 1
                if curr_cell == 0:
                    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                    # cell_type = sheet.cell_type(curr_row, curr_cell)
                    destinatarios_list.append(sheet.cell_value(curr_row, curr_cell+1))
        server = MicrosipMailServer()
        server.sendmail(destinatarios_list, asunto, mensaje)
        message = 'Correos envíados correctamente :D'
    context = {'mensaje': message, 'form': form, 'estatus': 'ok', }
    return render(request,template_name, context)
