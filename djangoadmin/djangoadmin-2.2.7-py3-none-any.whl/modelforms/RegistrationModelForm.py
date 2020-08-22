from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationModelForm(UserCreationForm):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder': 'Username'}))
    email = forms.CharField(max_length=30, widget=forms.EmailInput(attrs={"type":"email", "class":"form-control rounded-0", 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control rounded-0', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-control rounded-0', 'placeholder': 'Confirm password'}))

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']