# from django.conf.urls import patterns, url
from django.urls import path,include
from . import views

urlpatterns = (
    path('saldos/por_seleccion/', views.PorSeleccionView),
    path('saldos/todos/', views.mensajes_masivos),
    path('get_mensajes_saldos/', views.get_mensajes_saldos),
    path('enviar_mail_seleccion/', views.enviar_cargos_seleccion),
    path('saldos/enviar_por_vencer/', views.enviar_cargos_por_vencer),
    path('saldos_automaticos_preferencias/', views.saldos_automaticos_preferencias),
    path('saldos_por_vencer_automaticos_preferencias/', views.saldos_por_vencer_automaticos_preferencias),
    path('crear_archivo/', views.crear_archivo),
)
