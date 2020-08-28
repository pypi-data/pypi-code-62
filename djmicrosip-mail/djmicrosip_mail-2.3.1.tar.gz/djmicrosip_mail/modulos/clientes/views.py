#encoding:utf-8
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# user autentication
from .models import *
from .forms import *
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
import json


class ClienteListView(ListView):
    context_object_name = "clientes"
    model = Cliente
    template_name = 'djmicrosip_mail/clientes/clientes.html'
    paginate_by = 50

    def get_queryset(self):
        get_dict = self.request.GET
        form = ClienteSearchForm(self.request.GET)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            nombre = form.cleaned_data['nombre']
            clave = form.cleaned_data['clave']
            clientes = Cliente.objects.all()
            if nombre:
                clientes = clientes.filter(nombre__contains=nombre)
            if clave:
                claves = ClienteClave.objects.filter(clave=clave)
                if claves:
                    clientes = Cliente.objects.filter(pk=claves[0].cliente.id)
            if cliente:
                clientes = Cliente.objects.filter(pk=cliente.id)

        return clientes

    def get_context_data(self, **kwargs):
        context = super(ClienteListView, self).get_context_data(**kwargs)
        context['form'] = ClienteSearchForm(self.request.GET or None)
        return context


@login_required(login_url='/login/')
def IgnorarView(request):
    cliente_id = request.GET['cliente_id']
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if cliente.no_enviar_mail:
        cliente.no_enviar_mail = False
    else:
        cliente.no_enviar_mail = True
    cliente.save()
    data = {'cliente': cliente.nombre,
            }

    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')
