#----encoding:utf-8------------
from django import forms
from .models import *


def UpdateRegistry(registry_name, value):
    registry = Registry.objects.get(nombre=registry_name)
    registry.valor = value
    registry.save()


def UpdateRegistryLong(registry_name, value):
    registry = RegistryLong.objects.get(nombre=registry_name)
    registry.valor = value
    registry.save()


class PreferenciasManageForm(forms.Form):
    enviar_remisiones = forms.BooleanField(label='Enviar remisiones Pendientes', required=False)
    dias_atraso = forms.DecimalField(max_digits=10, decimal_places=3)
    monto_minimo = forms.DecimalField(max_digits=10, decimal_places=3)
    empresa_nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de empresa...'}))
    mensaje_extra = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}), required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Correo Elecrónico...'}))
    servidor = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección Servidor...'}))
    puerto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Puerto...'}))
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña...'}), required=False)

    def save(self, *args, **kwargs):
        UpdateRegistry('SIC_MAIL_EmpresaNombre', self.cleaned_data['empresa_nombre'])
        UpdateRegistry('SIC_MAIL_MontoMinimo', self.cleaned_data['monto_minimo'])
        UpdateRegistry('SIC_MAIL_DiasPorVencer', self.cleaned_data['dias_atraso'])
        UpdateRegistryLong('SIC_MAIL_MensajeExtra', self.cleaned_data['mensaje_extra'])

        UpdateRegistry('Email', self.cleaned_data['email'])

        enviar_remisiones = 'S' if self.cleaned_data['enviar_remisiones'] else 'N'
        UpdateRegistry('SIC_MAIL_EnviarRemisionesPendientes', enviar_remisiones)
        UpdateRegistry('SMTP_HOST', self.cleaned_data['servidor'])
        UpdateRegistry('SMTP_PORT', self.cleaned_data['puerto'])
        UpdateRegistry('SMTP_USERNAME', self.cleaned_data['usuario'])

        if self.cleaned_data['password']:
            UpdateRegistry('SMTP_PASSWORD', self.cleaned_data['password'])
