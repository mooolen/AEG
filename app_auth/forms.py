
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder': 'Username', 'autofocus':'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
