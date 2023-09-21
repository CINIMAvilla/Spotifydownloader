import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client, filters

YOUR_CLIENT_ID = "857ba4e2288e43bda42a43cf76fd84d3"
YOUR_CLIENT_SECRET = "a25b7d3b6b03437aa82870ef06dbd65d"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=YOUR_CLIENT_ID,
                                                           client_secret=YOUR_CLIENT_SECRET))
                                                
async def send_track(chat_id, track_info):
    track_name = track_info['name']
    artists = ', '.join(artist['name'] for artist in track_info['artists'])
    audio_url = track_info['preview_url']
    caption = f"🎵 Track: {track_name} by {artists}"
    await client.send_audio(chat_id=chat_id, audio=audio_url, caption=caption)

async def send_playlist_tracks(chat_id, playlist_tracks):
    for track_info in playlist_tracks:
        await send_track(chat_id, track_info['track'])

@Client.on_message(filters.regex(r'https?://open\.spotify\.com/(track|playlist)/[a-zA-Z0-9]+'))
async def handle_spotify_link(client, message):
    chat_id = message.chat.id
    link = message.matches[0].group(0)

    if 'track' in link:
        # Single track link
        track_id = link.split('/')[-1]
        track_info = sp.track(track_id)
        await send_track(chat_id, track_info)
    elif 'playlist' in link:
        # Playlist link
        playlist_id = link.split('/')[-1]
        playlist_info = sp.playlist_tracks(playlist_id)
        await send_playlist_tracks(chat_id, playlist_info['items'])
