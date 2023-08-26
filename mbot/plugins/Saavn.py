from pyrogram import Client, filters, types
import requests
import urllib.parse
import aiohttp
import asyncio


@Client.on_message(filters.text & (filters.private | filters.group))
async def search_and_send_song(client, message):
    query = urllib.parse.quote(message.text)
    if query.startswith("/"):
        return
        
    searching_msg = await message.reply("Searching...")
    url = f"https://saavn.me/search/songs?query={query}&page=1&limit=1"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
    except Exception as e:
        await searching_msg.delete()
        return

    try:
        result = r['data']['results'][0]
        sname = result['name']
        slink = result['downloadUrl'][4]['link']
        ssingers = result['primaryArtists']
        img = result['image'][2]['link']
        song_url = result['url']
        duration = result['duration']

        requester = message.from_user.username if message.from_user.username else "Someone"

        # Simulate the "downloading" status
        await searching_msg.edit("Downloading...")

        async with aiohttp.ClientSession() as session:
            async with session.get(img) as img_response:
                img_data = await img_response.read()
            async with session.get(slink) as song_response:
                song_data = await song_response.read()

        thumbnail_path = "thumbnail.jpg"
        song_path = "song.mp3"
        with open(thumbnail_path, "wb") as thumbnail_file, open(song_path, "wb") as song_file:
            thumbnail_file.write(img_data)
            song_file.write(song_data)

        # Simulate the "uploading" status
        await searching_msg.edit("Uploading...")

        await message.reply_audio(
            audio=song_path,
            title=sname,
            performer=ssingers,
            caption=f"🎵 [{sname}]({song_url})\n"
                    f"🕒 Duration: {duration}\n"
                    f"👤 Requested by: {requester}",
            thumb=thumbnail_path
        )

        os.remove(thumbnail_path)
        os.remove(song_path)

    except (KeyError, IndexError):
        await message.reply("No results found.")
        
    finally:
        await searching_msg.delete()
