from django.conf.urls import patterns, url
from hangouts import views

urlpatterns = patterns( '', 
	url(r'^$', views.index, name='index'),
	url(r'^playlist/$', views.playlist, name='playlist'),
)