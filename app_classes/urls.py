from django.conf.urls import patterns, url
from app_classes import views

urlpatterns = patterns('',
	url(r'^dashboard/$', views.dashboard),
	url(r'^classes/$', views.class_teacher, name='classes'),
	url(r'^classes/add/$', views.teacher_addNewClass),
	url(r'^classes/submit/$', views.submit),
	url(r'^classes/(?P<class_id>\d+)/edit/$', views.edit, name='edit'),
	url(r'^classes/checkManually/$', views.manualChecking),
	# ex: /polls/5/vote/
    url(r'^classes/(?P<class_id>\d+)/delete/$', views.delete, name='delete'),

)
