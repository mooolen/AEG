from django.conf.urls import patterns, url, include
from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
#from registration.views import activate
#from registration.views import register
from app_registration.forms import CustomRegistrationForm

urlpatterns = patterns('',
                       url(r'^accounts/register/$',
					   register,
					    {'backend': 'accounts.regbackend.RegBackend','form_class':CustomRegistrationForm},        
					    name='registration_register'
					    )
                       )