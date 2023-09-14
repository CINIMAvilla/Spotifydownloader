from pyrogram import Client, filters
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id="857ba4e2288e43bda42a43cf76fd84d3",
                                                   client_secret="a25b7d3b6b03437aa82870ef06dbd65d"))

@Client.on_message(filters.regex(r'https://open\.spotify\.com/track/([a-zA-Z0-9]+)'))
def get_spotify_info(client, update):
    spotify_track_url = update.text
    track_id = spotify_track_url.split("/")[-1]

    try:
        track_info = sp.track(track_id)
        track_name = track_info['name']
        artists = [artist['name'] for artist in track_info['artists']]

        saavn_url = get_saavn_link(track_name, artists)
        send_music_to_user(client, update.chat.id, saavn_url)
    except Exception as e:
        print(f"Error: {e}")
      
def get_saavn_link(track_name, artists):
    saavn_search_url = f"https://www.saavn.me/search/{track_name}-{artists[0]}/"
    response = requests.get(saavn_search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    saavn_url = soup.find("a", class_="btn btn-primary")['href']
    return saavn_url

def send_music_to_user(client, chat_id, saavn_url):
    response = requests.get(saavn_url)
    music_content = response.content
    client.send_audio(chat_id, audio=music_content, title="Music", performer="Artist")
