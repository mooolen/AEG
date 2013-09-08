
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'login-field', 'placeholder': 'Username', 'autofocus':'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login-field', 'placeholder':'Password'}))

class PasswordForm(forms.Form):
	OldPassword = forms.CharField( label='Old Password', widget=forms.PasswordInput(attrs={'type':'password', 'class': 'span3', 'placeholder': 'Required', 'name': 'newPassword'}))
	password = forms.CharField( label='Password', widget=forms.PasswordInput(attrs={'type':'password', 'class': 'span3', 'placeholder': 'Required', 'name': 'newPassword'}))
	ConfPassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'type':'password', 'class': 'span3', 'placeholder': 'Required', 'name':'confPassword'}))

