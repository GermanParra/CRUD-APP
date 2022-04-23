from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



# Get API keys from .env
SPOTIPY_CLIENT_ID = getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, CLIENT_SECRET))

def search_albums(input_string):
  '''Takes user's input string and pull the information for 5 related albums from the Spotify Database'''
  Albums = spotify.search(input_string, limit=5, offset=0, type='album', market=None)['albums']['items']
  return Albums


def get_albums_data(Albums):
  '''Takes results from 'search_albums' and extracts required info from albums
     ( id, artist, released, title, total_tracks)'''
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
  # albums_data[0] SAMPLE --> {'artist':'ABBA' ,'id':'2cKZfaz7GiGtZEeQNj1RyR' ,'released':'2008-01-01', 'title':'ABBA Gold', 'total_tracks':19}


def get_albums_tracks_data(albums_data):
  '''Takes results from 'get_albums_data' and extracts required info from tracks
     ( id, name, duration, player_src )'''
  albums_ids = [i['id'] for i in albums_data]
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
      track['player_src'] = f"https://open.spotify.com/embed/track/{song['id']}?utm_source=generator&theme=0"
      album.append(track)
    tracks_data.append(album)
  return tracks_data
  # tracks_data[0][0] SAMPLE --> {'duration': '3:51', 'id': '2ATDkfqprlNNe9mYWodgdc', 'name': 'Dancing Queen'}

def create_player_sources(tracks_data):
    '''Takes results from 'get_albums_tracks_data' and uses tracks id's
    to return a list with urls that can be use as source on Spotify players'''
    albums_ids = [i['id'] for i in tracks_data]
    sources = []
    for id in albums_ids:
        sources.append(f"https://open.spotify.com/embed/track/{id}?utm_source=generator&theme=0")
    return sources