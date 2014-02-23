# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
import soundcloud

# Index will contain a form for entering user information to generate the playlist.
def index(request):
	template = loader.get_template('hangouts/index.html')
	context = RequestContext(request, {},)
	return HttpResponse(template.render(context))

# Given a request, returns a list containing all the entered soundhound user ids.
def get_users(client, request):
	ids = []
	# Each user input has the name with the format user_name#.
	for key,val in request.POST.iteritems():
		if "user_name" in key:
			user_id = client.get('/resolve', url='https://soundcloud.com/' + val).id
			ids.append(user_id)
	return ids

def get_sorted_tracks(client, ids):
	fav_tracks = []
	playlists = []
	favs_pts = 10
	playlists_pts = 7

	track_ids = {}
	following_points = 2

	# Find all tracks that users have favourited.
	for user in ids:
		fav_tracks = fav_tracks + list(client.get('/users/' + str(user) + '/favorites'))
			
	# Count how many users have favourited each song.
	for t in fav_tracks:
		if t.id in track_ids:
			track_ids[t.id] += favs_pts
		else:
			track_ids[t.id] = favs_pts

	print "GET FOLLOWERS"
	# Get the list of users followed by each user. 
	following = []
	for user in ids:
		print "GET FOLLOWERS: USER " + str(user)
		following = following + list(client.get('/users/' + str(user) + '/followings'))

	print "GET TRACKS"
	# Get a list of tracks that each follower has created.
	tracks_by_following = []
	for f in following:
		tracks_by_following = tracks_by_following + list(client.get('/users/' + str(f.id) + '/tracks'))
	print tracks_by_following
	# Increase the rank for each track in the followers.
	for t in tracks_by_following:
		if t.id in track_ids:
			track_ids[t.id] += following_points
		else:
			track_ids[t.id] = following_points

	#Find all the playlists for each user
	for user in ids:
		playlists = playlists + list(client.get('/users/' + str(user) + '/playlists'))

	#Count how many user have a song in one of their playlists
	for p in playlists:
		print "Playlists: " 
		print "Tracks: "
		print p.tracks[0][u'id']
		for t in p.tracks:
			if t[u'id'] in track_ids:
				track_ids[t[u'id']] += playlists_pts
			else:
				track_ids[t[u'id']] = playlists_pts

	# Return a list of sorted track ids based on each songs rank.
	sorted_tracks = sorted(track_ids, key=track_ids.get)
	sorted_tracks.reverse()
	return sorted_tracks

# Playlist will contain a customized soundcloud playlist.
def playlist(request):
	client = soundcloud.Client( 
		client_id='d05accec0d8806ca775fd78523f6832a',
		client_secret='e78f9f003214b112a1160561089a9182',
		username='mike_n_7',
		password='pressplay'
	)

	users = get_users(client, request)
	ranked_tracks = get_sorted_tracks(client, users)

	tracks = map(lambda id: dict(id=id), ranked_tracks)
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