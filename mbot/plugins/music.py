from pyrogram import filters, Client
from youtube_search import YoutubeSearch
from youtube_dl import YoutubeDL

@Client.on_message(filters.command('song'))
def song(client, message):
    query = ' '.join(message.command[1:])
    m = message.reply("Searching for your song...")

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        duration = results[0]["duration"]

        ydl_opts = {"format": "bestaudio[ext=m4a]"}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)

        caption = f"""
**Title:** [{title}]({link})
**Duration:** {duration}
Requested by: {message.from_user.mention}
        """
        client.send_audio(
            chat_id=message.chat.id,
            audio=audio_file,
            caption=caption,
            parse_mode='md',
            quote=False,
            title=title,
            duration=duration,
        )
        m.delete()

    except Exception as e:
        m.edit("An error occurred while processing your request.")
        print(e)
