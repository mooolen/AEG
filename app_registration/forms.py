
from django.contrib.auth.models import User
from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from app_registration.models import CustomRegistrationProfile
from registration.models import RegistrationProfile
from app_auth.models import School

<<<<<<< HEAD
attrs_dict = { 'class': 'required' }
class CustomRegistrationForm(RegistrationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder': 'First Name', 'autofocus':'autofocus'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label=None)

	def save(self, profile_callback=None):
		new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
		password=self.cleaned_data['password1'],
		email=self.cleaned_data['email'])
		new_profile = CustomRegistrationProfile(user=new_user, first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'], school=self.cleaned_data['school'])
		new_profile.save()

		return new_user
=======
class RegistrationForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'login-field', 'placeholder':'User Name', 'autofocus':'autofocus'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'login-field', 'placeholder':'Email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'type':'text', 'class': 'login-field', 'placeholder': 'First Name',}))
>>>>>>> 7586f54da913d222fc53f1ec003d23ea73645156
