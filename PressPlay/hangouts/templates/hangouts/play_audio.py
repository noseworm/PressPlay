import soundcloud

# create a client object with your app credentials
client = soundcloud.Client(client_id='d05accec0d8806ca775fd78523f6832a')

# fetch track to stream
track = client.get('/tracks/293')

# get the tracks streaming URL
stream_url = client.get(track.stream_url, allow_redirects=False)

# print the tracks stream URL
print stream_url.location