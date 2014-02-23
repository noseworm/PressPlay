from django.db import models

# Contains information about a user (including artists).
class Users(models.Model):
	user_id = models.CharField(max_length=100)
	user_name = models.CharField(max_length=100)
	def __unicode__(self):
		return self.user_name

# Contains information about a track.
class Tracks(models.Model):
	track_id = models.CharField(max_length=100)
	track_title = models.CharField(max_length=100)
	genre = models.CharField(max_length=100)
	def __unicode__(self):
		return self.track_title

# Contains information about a playlist.
class Playlists(models.Model):
	playlist_id = models.CharField(max_length=100)
	def __unicode__(self):
		return self.playlist_id

# Contains the relationship between users and their favourite tracks.
class Favourites(models.Model):
	track = models.ForeignKey('Tracks')
	user = models.ForeignKey('Users')
	def __unicode__(self):
		return self.user.user_name + ' -> ' + self.track.track_title

# Cotnains the relationship between a song an its artist.
class ArtistOf(models.Model):
	track = models.ForeignKey('Tracks')
	user = models.ForeignKey('Users')
	def __unicode__(self):
		return self.user.user_name + ' -> ' + self.track.track_title

# Contains the relationship between a playlist and its tracks.
class TrackOnPlaylist(models.Model):
	track = models.ForeignKey('Tracks')
	playlist = models.ForeignKey('Playlists')
	def __unicode__(self):
		return self.playlist.playlist_id + ' -> ' + self.track.track_title

# Contains the relationship between a user and his/her followers.
class Following(models.Model):
	artist = models.ForeignKey('Users', related_name="artist")
	user = models.ForeignKey('Users', related_name="user")
	def __unicode__(self):
		return self.user.user_name + ' -> ' + self.artist.user_name

class UserPlaylist(models.Model):
	user = models.ForeignKey('Users')
	playlist = models.ForeignKey('Playlists')
	def __unicode__(self):
		return self.user.user_name + ' -> ' + str(self.playlist.playlist_id)

class Democracy(models.Model):
	thefineline = models.IntegerField(default=0)
	
