
from django.contrib.auth.models import User
from django import forms
from django.utils.html import strip_tags

class LoginForm(forms.Form):
<<<<<<< HEAD
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder': 'Username', 'autofocus':'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
=======
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder': 'Username',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
>>>>>>> f93d7213a3fe3570e6c2d4f2cb223a106252f3d9
