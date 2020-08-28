#----encoding:utf-8------------
from django import forms
from .models import *
import autocomplete_light.shortcuts as autocomplete_light
import os


class MailForm(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}))
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    destinatario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Para'}))
    imagen = forms.FileField(required=False)
    archivo = forms.FileField(required=False)


class MailAllForm(forms.Form):
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}))
    imagen = forms.FileField(required=False)
    archivo = forms.FileField(required=False)



class SelectMultipleClients(forms.Form):
    clientes = forms.ModelMultipleChoiceField(queryset=Cliente.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}))
    imagen = forms.FileField(required=False)
    archivo = forms.FileField(required=False)


class ZonaForm(forms.Form):
    zona = forms.ModelChoiceField(queryset=Zona.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}))
    imagen = forms.FileField(required=False)
    archivo = forms.FileField(required=False)

IMPORT_FILE_TYPES = ['.xls', '.xlsx', ]


class MailFileForm(forms.Form):
    archivo = forms.FileField()
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}))

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        extension = os.path.splitext(archivo.name)[1]
        if not (extension in IMPORT_FILE_TYPES):
            raise forms.ValidationError(u'%s No es un archivo de Excel valido. Por favor, asegurese de que su archivo de entrada es un archivo de Excel' % extension)
        else:
            return archivo
