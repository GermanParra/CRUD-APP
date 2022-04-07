from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Get Spotify API keys from .env
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))