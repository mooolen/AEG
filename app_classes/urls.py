from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),
<<<<<<< HEAD
	url(r'^class/$', views.class_list),
	url(r'^class/add$', views.add_class),
=======
	url(r'^class_teacher/$', views.class_teacher),
	url(r'^teacher_addNewClass/$', views.teacher_addNewClass),
>>>>>>> f93d7213a3fe3570e6c2d4f2cb223a106252f3d9
)
