from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),	
)
