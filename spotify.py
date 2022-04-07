from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from SpotiKeys import CLIENT_ID, CLIENT_SECRET


## Get API keys from .env
#CLIENT_ID = getenv('CLIENT_ID')
#CLIENT_SECRET = getenv('CLIENT_SECRET')


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))

def get_albums_data(Albums):
  albums_data = []
  for album in Albums:
    dic = {}
    dic['id'] = album['id']
    dic['title'] = album['name']
    dic['artist'] = album['artists'][0]['name']
    dic['released'] = album['release_date']
    dic['total_tracks'] = album['total_tracks']
    albums_data.append(dic)
  return albums_data


def get_albums_tracks_data(albums_ids):
  tracks_data = []
  for id in albums_ids:
    album = []
    for song in spotify.album_tracks(id)['items']:
      track = {}
      track['id'] = song['id']
      track['name'] = song['name']
      min = int((int(song['duration_ms'])/1000)/60)
      sec = int((((int(song['duration_ms'])/1000)/60) - min) * 60)
      track['duration'] = str(min)+':'+str(sec)
      album.append(track)
    tracks_data.append(album)
  return tracks_data