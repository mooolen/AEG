
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'login-field', 'placeholder':'User Name', 'autofocus':'autofocus'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'login-field', 'placeholder':'Email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'text', 'class': 'login-field', 'placeholder': 'First Name',}))