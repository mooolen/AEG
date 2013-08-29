from django.conf.urls import patterns, url
from app_student import views

urlpatterns = patterns('',
	url(r'^student_home/$', views.dashboard),
	url(r'^student_answerExam/$', views.student_answerExam),
)
