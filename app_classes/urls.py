from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),
	url(r'^class/$', views.class_list),
	url(r'^class/add$', views.add_class),
)
