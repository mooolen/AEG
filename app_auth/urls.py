from django.conf.urls import patterns, url
from app_auth import views

urlpatterns = patterns('',
	#url(r'^$', views.user_login, name='user_login'),
	url(r'^$', views.LoginView.as_view(), name='user_login'),
	url(r'^logout$', views.user_logout, name='user_logout'),
	# ex: /profile/5/
	url(r'^profile/$', views.profile_edit, name='profile'),
	url(r'^edit_password/$', views.password_edit, name='edit_password'),
	url(r'^saveGrades/$', views.saveGrades, name='saveGrades'),
	url(r'^help/$', views.help,  name='help'),
	url(r'^viewGradeSys/(?P<gradeSys_id>\d+)/$', views.viewGradeSys, name='grades'),
	url(r'^deleGradeSys/(?P<gradeSys_id>\d+)/$', views.deleGradeSys, name='deleGradeSys'),
)
