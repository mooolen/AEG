from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),
	url(r'^class_teacher/$', views.class_teacher),
	url(r'^teacher_addNewClass/$', views.teacher_addNewClass),
	url(r'^submit/$', views.submit),
)
