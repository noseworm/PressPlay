from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# Look in the hangouts url file.
    url(r'^', include('hangouts.urls', namespace="hangouts")),
)
