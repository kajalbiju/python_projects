from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import requests
import spotipy



CLIENT_ID = "ae734087881744d28ffc85f887a6df9c"
CLIENT_SECRET = "92efa4e8fa124d99b16fb6ce681c8cb7"
redirect_uri ="https://open.spotify.com/"
USER_ID = "r7sed0tvd9204uanjyy36xjwi"


# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri= redirect_uri,
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name= playlist_name, public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)