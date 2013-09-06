from django.conf.urls import patterns, url
from app_student import views

urlpatterns = patterns('',
	url(r'^home/$', views.home, name='home'),
	url(r'^answerExam/$', views.answerExam),
	url(r'^viewClasses/$', views.viewClasses),
	url(r'^editProfile/$', views.editProfile),
	url(r'^viewProfile/$', views.viewProfile),
	url(r'^viewEssays/$', views.viewEssays),
	url(r'^viewEssay/$', views.viewEssay),
)
