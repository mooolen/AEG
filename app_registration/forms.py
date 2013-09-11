
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder': 'First Name', 'autofocus':'autofocus'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))