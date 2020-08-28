#encoding:utf-8
from django import forms
import os


class MailForm(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe algo...'}))
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    destinatario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Para'}))



