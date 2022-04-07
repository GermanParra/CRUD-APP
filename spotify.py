from os import getenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from SpotiKeys import CLIENT_ID, CLIENT_SECRET


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))