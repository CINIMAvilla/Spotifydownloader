from yt_dlp import YoutubeDL
import os
from pyrogram import filters, enums, Client as Mbot
import shutil

async def download_songs(query, download_directory='.'):
    query = f"{query} Lyrics".replace(":", "").replace("\"", "")
    ydl_opts = {
        'format': "bestaudio/best",
        'default_search': 'ytsearch',
        'noplaylist': True,
        "outtmpl": f"{download_directory}/%(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            video_info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            if video_info is None:
                return "Track Not Found ⚠️"
            
            filename = ydl.prepare_filename(video_info)
            if not filename:
                return "Track Not Found ⚠️"
            
            path_link = filename
            return path_link
        except Exception as e:
            return f"An error occurred while fetching the song: {str(e)}"

    return video_info

@Mbot.on_message(
    filters.command('song') 
    & filters.text & filters.incoming
)
async def song(_, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        k = await message.reply("⌛")
        print ('⌛')
        try:
            randomdir = f"/tmp/{str(randint(1,100000000))}"
            os.mkdir(randomdir)
        except Exception as e:
            await message.reply_text(f"Failed to send song, retry after some time 😥 Reason: {e}")
            return await k.delete()

        query = message.text.split(None, 1)[1]
        await k.edit("Downloading")
        print('Downloading')
        await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
        path = await download_songs(query, randomdir)
        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await k.edit('Uploading')
        await message.reply_audio(path)

    except IndexError:
        await message.reply("Song requires an argument, e.g., /song faded")
        return await k.delete()
    except Exception as e:
        await message.reply_text(f"Failed to send song 😥 Reason: {e}")
    finally:
        try:
            shutil.rmtree(randomdir)
            await message.reply_text(f"Check out @c_i_n_i_m_a_v_i_l_l_a (movie group) @TOM_Auto_filter_bot (movie bot)")
            return await k.delete()
        except:
            pass
