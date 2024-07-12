from bs4 import BeautifulSoup
import requests
# import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import keys

## ------- SPOTIPY AUTH ---------- #

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=keys.SPOTIPY_CLIENT_ID,
                                               client_secret=keys.SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=keys.SPOTIPY_REDIRECT_URI,
                                               scope='playlist-modify-private'))

# user_id = sp.current_user()["id"]

playlist_name = "New private playlist"
playlist_description = "Private list test"


# ---------- CREATE PLAYLIST ON SPOTIFY ---------#
playlist = sp.user_playlist_create(user=keys.USER, name=playlist_name, public=False, description=playlist_description)

print(f"Created playlist: {playlist['name']}")
print(f"Playlist URL: {playlist['external_urls']['spotify']}")


playlists = sp.user_playlists('spotify')
print(playlists)


## ---------- LIST OF SONGS -------#

date_choice = input("Please enter your date in YYYY-MM-DD format: ")
# date_choice = "2000-08-12"
year = date_choice.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_choice}")

soup = BeautifulSoup(response.text, "html.parser")
print(soup.title)

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names)


## ---------- ADD ITEMS IN SPOTIFY PLAYLIST ----------#


## ---- search
search = sp.search(song_names)
playlist_src = []
# pprint(search["tracks"]["items"][0]["album"])

for n in range(10):
    release_date = search["tracks"]["items"][n]["album"]["release_date"].split("-")[0]
    print(release_date)
    if release_date == year:
        playlist_src.append(search["tracks"]["items"][n]["uri"])
print(playlist_src)

## ---- adding
sp.playlist_add_items(keys.playlist_id, playlist_src)
