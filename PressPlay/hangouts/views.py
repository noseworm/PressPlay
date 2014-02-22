# Create your views here.
from django.http import HttpResponse

# Index will contain a form for entering user information to generate the playlist.
def index(request):
	return HttpResponse("INDEX")

# Playlist will contain a customized soundcloud playlist.
def playlist(request):
	return HttpResponse("PLAYLIST")