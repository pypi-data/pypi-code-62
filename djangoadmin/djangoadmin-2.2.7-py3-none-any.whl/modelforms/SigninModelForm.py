from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class SigninModelForm(AuthenticationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control rounded-0', 'placeholder': 'Password'}))

    class Meta:
        model  = User
        fields = ['username', 'password']