# from django.conf.urls import patterns, url
from django.urls import path,include
from .views import preferencias_view, preparar_aplicacion

urlpatterns = (
	path('preferencias/', preferencias_view),
	path('preparar_aplicacion/', preparar_aplicacion),
)
