
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder': 'First Name', 'autofocus':'autofocus'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
	repassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Retype Password'}))
	street = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Street'}))
	province = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Province'}))
	municipality = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Municipality'}))
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
