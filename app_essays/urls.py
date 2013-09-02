from django.conf.urls import patterns, url
from app_essays import views

urlpatterns = patterns('',
	url(r'^essays/new/$', views.new_essay, name='new'),
	url(r'^essays/$', views.list_essay, name='list'),
)
