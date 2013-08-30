from django.conf.urls import patterns, include, url
from django.contrib import admin
from AEG import settings
admin.autodiscover()

urlpatterns = patterns('',
	#url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('app_auth.urls', namespace='auth')),
	url(r'^', include('app_classes.urls')),
<<<<<<< HEAD
	url(r'^', include('app_student.urls')),
	url(r'^search/', include('haystack.urls'), name='haystack_search')
=======
>>>>>>> master
)

