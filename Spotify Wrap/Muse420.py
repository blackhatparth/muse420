import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import gspread
import datetime

SPOTIPY_CLIENT_ID = '5ccbfcd1a8fe44479be296cbfb6f8b55'
SPOTIPY_CLIENT_SECRET = 'b453b4ed4506472396e7eaf6bd4061b6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090/'
SCOPE = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

results = sp.current_user_top_tracks()
top_tracks_short = sp.current_user_top_tracks(limit=10, offset=0, time_range="short_term")
top_tracks_short

def get_track_ids(time_frame):
    track_ids = []
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids


track_ids = get_track_ids(top_tracks_short)
track_ids

def get_track_features(id):
    meta = sp.track(id)
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info

track_id = '4slSrbTK1sNK4I1mDYEthf'
get_track_features(track_id)

def convert_to_df(track_ids):
# loop over track ids 
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)
        # create dataset
        df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])
        # save to CSV
        df.to_csv(f'{time}-{datetime}.csv')

gc = gspread.service_account(filename='muse420-e14cc32d7b8d.json')
sh = gc.open("Muse420")
worksheet = sh.worksheet("short_term")
val = worksheet.acell('B5').value
print(val)

 


