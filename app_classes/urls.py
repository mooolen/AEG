from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),
	url(r'^classes/$', views.class_teacher),
	url(r'^classes/add/$', views.teacher_addNewClass),
	url(r'^classes/submit/$', views.submit),
<<<<<<< HEAD
	url(r'^classes/edit/$', views.edit),
=======
	url(r'^classes/checkManually/$', views.manualChecking),
>>>>>>> 3a24bf539ec1dc2d9c265f68db25d37a552a8c22
)
