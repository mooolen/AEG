try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

except ImportError:     # Python 2
    from urlparse import urlparse
    
from django.shortcuts import render_to_response, render
from django.conf import settings
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import (
	REDIRECT_FIELD_NAME, login, logout, authenticate
)
from  django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User, check_password
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.core.context_processors import csrf
from app_auth.models import UserProfile, passwordForm
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, PasswordForm

class LoginView(FormView):
	form_class = LoginForm
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'app_auth/login.html'
	success_url = '/dashboard'
	
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(LoginView, self).dispatch(request, *args, **kwargs)
	
	def form_valid(self, form, request):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
			
		user = authenticate(username=username, password=password)
			
		if user is not None:
			if user.is_active:
				login(self.request, user)
				return HttpResponseRedirect(self.get_success_url())			
		else:		
			return self.form_invalid(form, request)
	
	def form_invalid(self, form, request):
		return render_to_response( self.template_name , {
			'errors': 1,
			'form' : form, 
		},  RequestContext(request))
	
	def get_success_url(self):
		if self.success_url:
			redirect_to = self.success_url
		else:
			redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

		netloc = urlparse(redirect_to)[1]
		
		if not redirect_to:
			redirect_to = settings.LOGIN_REDIRECT_URL
		elif netloc and netloc != self.request.get_host():
			redirect_to = settings.LOGIN_REDIRECT_URL
		return redirect_to
	  
	def post(self, request, *args, **kwargs):
		c = {}
		c.update(csrf(request))
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		
		if form.is_valid():
			return self.form_valid(form, request)
		else:				
			return self.form_invalid(form, request)

def user_logout(request):
    return logout_then_login(request,login_url='/')

@login_required(redirect_field_name='', login_url='/')
def profile_edit(request, success=None):
	user_info = UserProfile.objects.get(user_id = request.user.id)
	avatar = user_info.avatar
	return render(request, 'app_auth/profile.html', {'avatar': avatar, 'user_info':user_info, 'success':success})

@login_required(redirect_field_name='', login_url='/')
def password_edit(request, err=None):
	user_info = UserProfile.objects.get(user_id = request.user.id)
	avatar = user_info.avatar
	form = PasswordForm()
	return render(request, 'app_auth/changePassword.html', {'avatar': avatar, 'user_info':user_info, 'form':form, 'error': err})

@login_required(redirect_field_name='', login_url='/')
def reset(request):
	form_class = PasswordForm(data=request.POST)
	if form_class.is_valid():
		forms = form_class.cleaned_data
		password = forms['password']
		newPassword = forms['ConfPassword']
		oldPassword = forms['OldPassword']
		u = User.objects.get(id=request.user.id)

	if u.check_password(oldPassword) and password == newPassword:
		u.set_password(newPassword)
		u.save()
		return profile_edit(request, 'You have changed your password.')
	else:
		return password_edit(request, 'Passwords did not matched.')

