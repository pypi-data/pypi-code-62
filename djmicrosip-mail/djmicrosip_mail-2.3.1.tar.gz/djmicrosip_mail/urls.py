# from django.conf.urls import patterns, url, include
from django.urls import path,include
from .views import index, envia_saldos_automaticos

from .modulos.clientes import urls as clientes_urls
from .modulos.personalizados import urls as personalizados_urls
from .modulos.saldos_clientes import urls as saldos_clientes_urls
from .modulos.herramientas import urls as herramientas_urls


urlpatterns =(
	path('', index),
	path('saldos/todos_automatico/', envia_saldos_automaticos),
	
	path('',include(clientes_urls)),
	path('',include(personalizados_urls)),
	path('',include(saldos_clientes_urls)),
	path('',include(herramientas_urls)),
)

