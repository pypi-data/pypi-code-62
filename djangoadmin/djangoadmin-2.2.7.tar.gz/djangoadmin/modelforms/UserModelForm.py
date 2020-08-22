from django import forms
from django.forms import ModelForm
from djangoadmin.models import UserModel


class UserModelForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ['image', 'address', 'phone', 'website']

        labels = {
            'image': 'Profile image',
            'address': 'Address',
            'phone': 'Phone',
            'website': 'Website',
        }

        widgets = { 
            'image': forms.ClearableFileInput(attrs={}),
            'address': forms.TextInput(attrs={'type': 'text', 'class': 'form-control rounded-0', 'placeholder': 'Address'}),
            'phone': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control rounded-0', 'placeholder': 'Phone'}),
            'website': forms.URLInput(attrs={'type': 'url', 'class': 'form-control rounded-0', 'placeholder': 'Website'})
        }