#encoding:utf-8
from microsip_api.comun.sic_db import get_conecctionname,first_or_none
from django.shortcuts import render_to_response,render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# user autentication
from .models import *
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from .procedures import procedures as procedures_sic
from django.db import connections, router
from django.core import management
from ...config import configuration_registers, configuration_register_longs

@login_required(login_url='/login/')
def preferencias_view(request, template_name='djmicrosip_mail/herramientas/preferencias.html'):
    
    form_initial = {
        'empresa_nombre': Registry.objects.get(nombre='SIC_MAIL_EmpresaNombre').get_value(),
        'monto_minimo': Registry.objects.get(nombre='SIC_MAIL_MontoMinimo').get_value(),
        'enviar_remisiones': Registry.objects.get(nombre='SIC_MAIL_EnviarRemisionesPendientes').get_value() == 'S',
        'mensaje_extra': RegistryLong.objects.get(nombre='SIC_MAIL_MensajeExtra').valor,
        'servidor': Registry.objects.get(nombre='SMTP_HOST').get_value(), 
        'puerto': Registry.objects.get(nombre='SMTP_PORT').get_value(), 
        'usuario': Registry.objects.get(nombre='SMTP_USERNAME').get_value(), 
        'password': Registry.objects.get(nombre='SMTP_PASSWORD').get_value(), 
        'email': Registry.objects.get(nombre='Email').get_value(), 
        'dias_atraso': Registry.objects.get(nombre='SIC_MAIL_DiasPorVencer').get_value(), 
    }

    form = PreferenciasManageForm(request.POST or None, initial = form_initial)
    msg = ''
    if form.is_valid():
        form.save()
        msg = 'Informacion actualizada'
 
    c ={'form':form, 'msg':msg,}
    return render(request,template_name, c)

@login_required( login_url = '/login/' )
def preparar_aplicacion(request):
    """ Agrega campos nuevos en tablas de base de datos. """
    padre = first_or_none(Registry.objects.filter(nombre='PreferenciasEmpresa'))
    if request.user.is_superuser and padre:
        
        using = router.db_for_write(Registry)
        for procedure  in procedures_sic:
            c = connections[using].cursor()
            c.execute(procedures_sic[procedure])
            c.execute('EXECUTE PROCEDURE %s;'%procedure)
            c.execute('DROP PROCEDURE %s;'%procedure)
            c.close()
            
        management.call_command( 'syncdb', database = using, interactive= False)       

        for register in configuration_registers:
            if not Registry.objects.filter(nombre = register).exists():
                Registry.objects.create(
                    nombre = register,
                    tipo = 'V',
                    padre = padre,
                    valor= '',
                )

        for register_long in configuration_register_longs:
            if not RegistryLong.objects.filter(nombre = register_long).exists():
                RegistryLong.objects.create(
                    id= -1,
                    nombre = register_long,
                    valor= '',
                )
                
    return HttpResponseRedirect('/mail/preferencias/')
