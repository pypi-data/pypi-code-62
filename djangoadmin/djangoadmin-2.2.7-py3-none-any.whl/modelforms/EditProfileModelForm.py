from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class EditProfileModelForm(UserChangeForm):
    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
            'password': 'Password'
        }

        widgets = { 
            'username': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'type': 'email', 'class': 'form-control rounded-0', 'placeholder': 'Email'})
        }