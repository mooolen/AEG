from django.conf.urls import patterns, url
from app_registration import views

urlpatterns = patterns('',
	url(r'^register/$', views.register, name='register'),
)
