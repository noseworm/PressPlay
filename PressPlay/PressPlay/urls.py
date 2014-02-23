from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Look in the hangouts url file.
    url(r'^', include('hangouts.urls', namespace="hangouts")),
    url(r'^admin/', include(admin.site.urls)),
)
