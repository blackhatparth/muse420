import streamlit as st
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import plotpolar

import recommendationengine

import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
#img = Image.open('muse420-streamlitapp/MUSE420LOGO.png')
#st.set_page_config(page_title="muse420",page_icon = img)

PAGE_CONFIG = {"page_title":'MUSE 420',"page_icon":"fire","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

SPOTIPY_CLIENT_ID = '5ccbfcd1a8fe44479be296cbfb6f8b55'
SPOTIPY_CLIENT_SECRET = 'b453b4ed4506472396e7eaf6bd4061b6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090/'
SCOPE = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

st.header("MUSE 420")
st.sidebar.radio("MENU",["Home","Contact","About Us"])
search_option = ['Tracks', 'Artists', 'Albums']
search_process = st.sidebar.selectbox("Select options to search: ",search_option)

keyword_search = st.text_input(search_process + " (Search your beloved thing)")
search_button = st.button("SEARCH")

search_result = []
if keyword_search is not None and len(str(keyword_search)) > 0 :
    if search_process == "Tracks":
        st.write("Finding your Track")
        tracks = sp.search(q='tracks:'+ keyword_search,type='track', limit=20)
        track_list = tracks['tracks']['items']
        if len(track_list) > 0:
            for track in track_list:
                #st.write(track['name'] + " - By - " + track['artists'][0]['name'])
                search_result.append(track['name'] + " - By - " + track['artists'][0]['name'])
    elif search_process == "Artists":
        st.write("Finding your Artist")
        artists = sp.search(q='artist:'+ keyword_search,type='artist', limit=20)
        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for artist in artists_list:
                #st.write(artist['name'])
                search_result.append(artist['name'])
    elif search_process == "Albums":
        st.write("Finding your Album")
        albums = sp.search(q='album:'+ keyword_search,type='album', limit=20)
        albums_list = albums['albums']['items']
        if len(albums_list) > 0:
            for album in albums_list:
                #st.write(album['name'] + " - By - " + album['artists'][0]['name'])
                search_result.append(album['name'] + " - By - " + album['artists'][0]['name'])

selected_track = None
selected_artist = None
selected_album = None    
if search_process == "Tracks":
    selected_track = st.selectbox("Your Selected Track:", search_result)
elif search_process == "Artists":
    selected_track = st.selectbox("Your Selected Artist:", search_result)
elif search_process == "Albums":
    selected_track = st.selectbox("Your Selected Album:", search_result)


if selected_track is not None and len(track) > 0:
    track_list = tracks['tracks']['items']
    track_id = None
    if len(track_list) > 0:
        for track in track_list:
            str_temp = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][1]['url']
                # st.write(track_id,track_album,img_album)
    selected_user_choice = None   
    if track_id is not None:
        user_choices = ['Song Features','Recommended Songs']
        selected_user_choice = st.sidebar.selectbox('Select your Choice',user_choices)
        if selected_user_choice == 'Song Features':
            track_features = sp.audio_features(track_id)
            df = pd.DataFrame(track_features, index=[0])
            df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']] 
            st.dataframe(df_features)
            plotpolar.feature_plot(df_features)
        elif selected_user_choice == 'Recommended Songs':
            token = recommendationengine.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
            token_json_response = recommendationengine.get_track_recommendations(track_id, token)
            recom_song = token_json_response['tracks']
            recom_song_df = pd.DataFrame(recom_song)
            st.write('Recommended Songs List:')
            st.dataframe(recom_song_df)
            recomdf_short = recom_song_df[['Name','Explicit']]
            

    else:
        st.write("Select track from the list:")
