"""MIT License

Copyright (c) 2022 Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.raw.functions import Ping
from mbot import LOG_GROUP, OWNER_ID, SUDO_USERS, Mbot,AUTH_CHATS
from os import execvp,sys
from mbot.plugins.Saavn import user_collection

@Mbot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        f"Hello {message.from_user.first_name}, I'm a Simple Music Downloader Bot. I Currently Support Download from Youtube.",
    )
    user_id = message.from_user.id
    is_subscribed = user_collection.find_one({'user_id': user_id})

    if not is_subscribed:
        user_collection.insert_one({"user_id": user_id})
        data = await client.get_me()
        BOT_USERNAME = data.username
        await message.reply(
            f"Please start the bot in a private chat by messaging @{BOT_USERNAME} and try again."
        )
        return
    await client.send_message(
        LOG_GROUP,
        f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={user_id}) started @{BOT_USERNAME} from PM!"
    )

@Mbot.on_message(filters.command("restart") & filters.chat(OWNER_ID) & filters.private)
async def restart(_,message):
    await message.delete()
    execvp(sys.executable,[sys.executable,"-m","mbot"])

@Mbot.on_message(filters.command("log") & filters.chat(SUDO_USERS))
async def send_log(_,message):
    await message.reply_document("bot.log")

@Mbot.on_message(filters.command("ping"))
async def ping(client,message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    ms = (datetime.now() - start).microseconds / 1000
    await message.reply_text(f"**Pong!**\nResponse time: `{ms} ms`")

HELP = {
    "Youtube": "Send **Youtube** Link in Chat to Download Song.",
    "Spotify": "Send **Spotify** Track/Playlist/Album/Show/Episode's Link. I'll Download It For You.",
    "Deezer": "Send Deezer Playlist/Album/Track Link. I'll Download It For You.",
    "Jiosaavn": "Not Implemented yet",
    "SoundCloud": "Not Implemented yet",
    "Group": "Will add later."
}


@Mbot.on_message(filters.command("help"))
async def help(_,message):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]

    await message.reply_text(f"Hello **{message.from_user.first_name}**, I'm **@spotify_downloa_bot**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))

@Mbot.on_callback_query(filters.regex(r"help_(.*?)"))
async def helpbtn(_,query):
    i = query.data.replace("help_","")
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Back",callback_data="helphome")]])
    text = f"Help for **{i}**\n\n{HELP[i]}"
    await query.message.edit(text = text,reply_markup=button)

@Mbot.on_callback_query(filters.regex(r"helphome"))
async def help_home(_,query):
    button = [
        [InlineKeyboardButton(text=i, callback_data=f"help_{i}")] for i in HELP
    ]
    await query.message.edit(f"Hello **{query.from_user.first_name}**, I'm **@NeedMusicRobot**.\nI'm Here to download your music.",
                        reply_markup=InlineKeyboardMarkup(button))
