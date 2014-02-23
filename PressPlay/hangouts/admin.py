from django.contrib import admin
from hangouts.models import Users, Tracks, Playlists, Favourites, ArtistOf, TrackOnPlaylist, UserPlaylist, Following, Democracy


admin.site.register(Users)
admin.site.register(Playlists)
admin.site.register(Tracks)
admin.site.register(Favourites)
admin.site.register(ArtistOf)
admin.site.register(TrackOnPlaylist)
admin.site.register(UserPlaylist)
admin.site.register(Following)