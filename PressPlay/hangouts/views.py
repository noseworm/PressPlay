# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
import soundcloud

# Index will contain a form for entering user information to generate the playlist.
def index(request):
	template = loader.get_template('hangouts/index.html')
	context = RequestContext(request, {},)
	return HttpResponse(template.render(context))

# Playlist will contain a customized soundcloud playlist.
def playlist(request):
	client = soundcloud.Client( 
		client_id='d05accec0d8806ca775fd78523f6832a',
		client_secret='e78f9f003214b112a1160561089a9182',
		username='mike_n_7',
		password='pressplay'	
	)

	user_id1 = client.get('/resolve', url='https://soundcloud.com/' + request.POST['user1_name']).id
	user_id2 = client.get('/resolve', url='https://soundcloud.com/' + request.POST['user2_name']).id
	fav1 = client.get('/users/' + str(user_id1) + '/favorites')
	fav2 = client.get('/users/' + str(user_id2) + '/favorites')

	track_ids1 = []
	track_ids2 = []
	for f in fav1:
		track_ids1.append(f.id)
	for f in fav2:
		track_ids2.append(f.id)

	print track_ids1
	print track_ids2
	track_ids = []
	for t in track_ids1:
		if t in track_ids2:
			track_ids.append(t)
	print track_ids

	tracks = map(lambda id: dict(id=id), track_ids)
	playlist = client.post('/playlists', playlist={
		'title': 'New playlist',
		'sharing': 'public',
		'tracks': tracks
	})

	embed_info = client.get('/oembed', url=str(playlist.permalink_url))
	template = loader.get_template('hangouts/playlists.html')
	context = RequestContext(request, {'embed_playlist': embed_info.html},)
	return HttpResponse(template.render(context))

def callback(request):
	template = loader.get_template('hangouts/callback.html')
	context = RequestContext(request, {},)
	return HttpResponse(template.render(context))