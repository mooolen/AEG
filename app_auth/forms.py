
from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'login-field', 'placeholder': 'Username', 'autofocus':'autofocus'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'login-field', 'placeholder':'Password'}))

class PasswordForm(forms.Form):
	OldPassword = forms.CharField( label='Old Password', widget=forms.PasswordInput(attrs={'type':'password', 'class': 'span3', 'placeholder': 'Required', 'name': 'newPassword'}))
	password = forms.CharField( label='Password', widget=forms.PasswordInput(attrs={'type':'password', 'class': 'span3', 'placeholder': 'Required', 'name': 'newPassword'}))
	ConfPassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'type':'password', 'class': 'span3', 'placeholder': 'Required', 'name':'confPassword'}))

class ProfileForm(forms.Form):
	last_name = forms.CharField( label='Last Name', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required', 'style':'color: #099'}))
	first_name = forms.CharField( label='First Name', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required', 'style':'color: #099'}))
	username = forms.CharField( label='Username', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required', 'style':'color: #099'}))
	email = forms.CharField( label='Email', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required', 'style':'color: #099'}))
	street = forms.CharField( label='Street', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required'}))
	municipality = forms.CharField( label='Municipality', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required'}))
	province = forms.CharField( label='Province', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required'}))
	phone_number = forms.CharField( label='Phone Number', widget=forms.TextInput(attrs={'type':'text', 'class': 'span3', 'placeholder': 'Required'}))
	avatar = forms.ImageField(label='Avatar', widget=forms.ClearableFileInput(attrs={'type':'file', 'class':'filestyle span3'}))