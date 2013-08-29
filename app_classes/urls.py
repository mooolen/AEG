from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),
	url(r'^classes/$', views.class_teacher),
	url(r'^classes/add/$', views.teacher_addNewClass),
	url(r'^classes/submit/$', views.submit),
)
