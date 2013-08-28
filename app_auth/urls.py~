from django.conf.urls import patterns, url
from app_auth import views


urlpatterns = patterns('',
	#url(r'^$', views.user_login, name='user_login'),
	url(r'^$', views.LoginView.as_view(), name='user_login'),
	url(r'^logout$', views.user_logout, name='user_logout'),
	url(r'^login$', views.LoginView.as_view(), name='login'),
)
