from django.db import models

# Contains information about a user (including artists).
class Users(models.Model):
	user_id = models.CharField(max_length=100)
	user_name = models.CharField(max_length=100)

# Contains information about a track.
class Tracks(models.Model):
	track_id = models.CharField(max_length=100)
	track_title = models.CharField(max_length=100)
	genre = models.CharField(max_length=100)

# Contains information about a playlist.
class Playlists(models.Model):
	playlist_id = models.CharField(max_length=100)

# Contains the relationship between users and their favourite tracks.
class Favourites(models.Model):
	track = models.ForeignKey('Tracks')
	user = models.ForeignKey('Users')

# Cotnains the relationship between a song an its artist.
class ArtistOf(models.Model):
	track = models.ForeignKey('Tracks')
	user = models.ForeignKey('Users')

# Contains the relationship between a playlist and its tracks.
class TrackOnPlaylist(models.Model):
	track = models.ForeignKey('Tracks')
	playlist = models.ForeignKey('Playlists')

# Contains the relationship between a user and his/her followers.
class Following(models.Model):
	artist = models.ForeignKey('Users', related_name="artist")
	user = models.ForeignKey('Users', related_name="user")

class UserPlaylist(models.Model):
	user = models.ForeignKey('Users')
	plalist = models.ForeignKey('Playlist')