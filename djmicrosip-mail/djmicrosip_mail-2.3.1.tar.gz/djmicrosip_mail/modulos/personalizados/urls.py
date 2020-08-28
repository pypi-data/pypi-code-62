# from django.conf.urls import patterns
from django.urls import path,include
from .views import todos_view, PorSeleccionView, zona_view, abierto_view, archivo_view

urlpatterns = (
	path('personalizados/todos/', todos_view),
	path('personalizados/por_seleccion/', PorSeleccionView),	
	path('personalizados/por_zona/', zona_view),
	path('personalizados/abierto/', abierto_view),
	path('personalizados/archivo/', archivo_view),
)
