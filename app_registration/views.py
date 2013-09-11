#from app_registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		#registration_form = RegistrationForm()
		if form.is_valid():
			#new_user=User.objects.create_user(self.cleaned_data['username'],
		   #                               self.cleaned_data['email'],
		   #                               self.cleaned_data['password1'])
			#new_user.first_name = self.cleaned_data['first_name']
			#new_user.last_name = self.cleaned_data['last_name']
			new_user = form.save()
			return HttpResponseRedirect("/")

	else:
		form = UserCreationForm()
	return render(request, "app_registration/register.html", {
        #'RegistrationForm' : registration_form,
        'form': form
    })