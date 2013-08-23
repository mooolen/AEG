import urlparse

from django.conf import settings
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login, logout, authenticate
)
from  django.contrib.auth.views import logout_then_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from .forms import LoginForm

class LoginView(FormView):
    form_class = LoginForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'app_auth/login.html'
    success_url = '/dashboard'
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
            
        user = authenticate(username=username, 
                            password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
        else:        
            return self.form_invalid(form)
    
    def form_invalid(self):
        return HttpResponseRedirect(reverse('app_name:login'))
    
    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to
      
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:                
            return self.form_invalid()
def user_logout(request):
	return logout_then_login(request,login_url='/')