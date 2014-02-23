# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from hangouts.models import Users, Tracks, Playlists, Favourites, ArtistOf, TrackOnPlaylist, UserPlaylist, Following
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

def populate_user(client, user_name):
	user_id = str(client.get('/resolve', url='https://soundcloud.com/' + user_name).id)
	user = Users(user_id=user_id, user_name=user_name)
	user.save()

	favourites = list(client.get('/users/' + user_id + '/favorites'))
	print "GOT FAVOURITES: " + str(len(favourites))
	for fav in favourites:
		# Create track if it doesn't already exist in the database.

		print "SEARCHING FOR TRACK..."
		tracks3 = Tracks.objects.filter(track_id=str(fav.id))
		if len(tracks3) == 0:
			print "ADDING TRACK..."
			try:
				title=fav.title
			except:
				title=""
			try:
				genre=fav.genre
			except:
				genre=""
			t3 = Tracks(track_id=str(fav.id), track_title=title, genre=genre)
			t3.save()
		else:
			t3 = tracks3[0]
		# Create a favourite relationship.
		fav_rel = Favourites(user=user, track=t3)
		fav_rel.save()

	playlists = list(client.get('/users/' + str(user.user_id) + '/playlists'))
	for plist in playlists:
		# Create playlist.
		playlist = Playlists(playlist_id=str(plist.id))
		playlist.save()
		# Create relationship between user and playlist.
		for t in plist.tracks:
			# Create track if it doesn't already exist in the database.
			tracks2 = Tracks.objects.filter(track_id=str(t[u'id']))
			if len(tracks2) == 0:
				print "ADDING TRACK..."
				try:
					title=t.title
				except:
					title=""
				try:
					genre=t.genre
				except:
					genre=""
				t2 = Tracks(track_id=str(t[u'id']), track_title=title, genre=genre)
				t2.save()
			else:
				t2 = tracks2[0]
			# Create relationship between playlist and track.
			playlist_track = TrackOnPlaylist(track=t2, playlist=playlist)
			playlist_track.save()

	following = list(client.get('/users/' + str(user.user_id) + '/followings'))
	for fol in following:
		# Create artist if it doesn't already exist.
		artists = Users.objects.filter(user_id=str(fol.id))
		if len(artists) == 0:
			print "ADDING ARTIST..."
			artist = Users(user_id=str(fol.id), user_name=fol.username)
			artist.save()
		else:
			artist = artists[0]
		# Create relationship between artist and user.
		following = Following(user=user, artist=artist)
		following.save()

		tracks1 = list(client.get('/users/' + str(fol.id) + '/tracks'))
		for t in tracks1:
			# Create track if it doesn't already exist.
			ts = Tracks.objects.filter(track_id=str(t.id))
			if len(ts) == 0:
				print "ADDING TRACK..."
				try:
					title=t.title
				except:
					title=""
				try:
					genre=t.genre
				except:
					genre=""
				t1 = Tracks(track_id=str(t.id), track_title=title, genre=genre)
				t1.save()
			else:
				t1 = ts[0]
			# Create relationship between artist and track.
			artist_of = ArtistOf(user=artist, track=t1)
			artist_of.save()

def get_sorted_tracks():
	fav_tracks = []
	playlists = []
	favs_pts = 10
	playlists_pts = 7
	following_points = 2
	max_tracks = 50

	track_ids = {}

	# Find all tracks that users have favourited.
	favourites = Favourites.objects.order_by('track__track_title')
	for t1 in favourites:
		fav_tracks.append(t1.track)
	
	# Count how many users have favourited each song.
	for t in fav_tracks:
		print t.track_id, t.track_title
		if t.track_id in track_ids:
			track_ids[t.track_id] += favs_pts
		else:
			track_ids[t.track_id] = favs_pts

	#Find all the playlists for each user
	#Count how many user have a song in one of their playlists
	tracks_on_playlists = TrackOnPlaylist.objects.order_by('track__track_title')
	for p in tracks_on_playlists:
		if p.track.track_id in track_ids:
			track_ids[p.track.track_id] += playlists_pts
		else:
			track_ids[p.track.track_id] = playlists_pts


	#If we have enough songs, we don't need to get followings
	if len(track_ids) < max_tracks: 
		tracks_by_following = ArtistOf.objects.order_by('track__track_title')
		# Increase the rank for each track in the followers.
		for t in tracks_by_following:
			if t.track.track_id in track_ids:
				track_ids[t.track.track_id] += following_points
			else:
				track_ids[t.track.track_id] = following_points

	#Establishes a threshold (average)
	sum_pts = 0
	for val in track_ids.values():
		sum_pts += val
	
	threshold = sum_pts/len(track_ids)

	#If a song has an under average ranking, it's deleted from the playlist
	for key in track_ids.keys():
		if track_ids[key] < threshold:
			del track_ids[key]

	# Return a list of sorted track ids based on each songs rank.

	print track_ids
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

	for key,val in request.POST.iteritems():
		if "user_name" in key:
			if len(Users.objects.filter(user_name=str(val))) == 0:
				populate_user(client, val)

	ranked_tracks = get_sorted_tracks()

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

