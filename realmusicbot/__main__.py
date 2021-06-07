"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import telebot
from random import choice
from time import sleep
import logging
import os
import platform
from . import settings
from . import commands
from . import keyboards
from . import music_provider
from . import utils

if platform.system() == "Windows":
    os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]
import mpv

if settings.radio:
    from . import radio_provider
if settings.genius_token:
    from . import lyrics_provider

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] (%(funcName)s) %(message)s",
    handlers=[logging.StreamHandler()],
)


def mpv_log(loglevel, component, message):
    print("[{}] ({}) {}".format(loglevel, component, message))


bot = telebot.TeleBot(settings.token, threaded=settings.threaded)
player = mpv.MPV(vid=False, ytdl=False, log_handler=mpv_log)


def send_msg(text, id, pic=None, keyboard=None):
    if isinstance(keyboard, tuple):  # custom inline keyboard
        keyboard = keyboards.create(keyboard)

    if pic:
        text += f"\n\n{pic}"
    try:
        if len(text) > 4000:
            send_msg(text[:4000], id)
            text = text[4000:]
        bot.send_message(id, text, reply_markup=keyboard)
    except Exception as e:
        logging.info(e)
        sleep(1)
        send_msg(text, id, keyboard=keyboard)


class Queue(object):
    queue = []

    def add(self, track):
        self.queue.append(track)
        if self.len > 1:
            Announcer.add_to_queue(track)
        else:
            self.now.play()
        logging.info("Added to queue: " + track.title)

    def skip(self):
        self.queue.pop(0)
        if self.len > 0:
            self.now.play()
        else:
            player.stop()

    def stop(self):
        self.queue.clear()
        player.stop()

    @property
    def now(self):
        return self.queue[0]

    @property
    def len(self):
        return len(self.queue)

    def items(self):
        if self.len == 0:
            return []
        items = []
        state = "⏸ Paused: " if player.pause else "🎶 Now playing: "
        elapsed = player.time_pos
        items.append(state + self.queue[0].to_string(elapsed=elapsed))
        for index, item in enumerate(self.queue[1:]):
            items.append(str(index + 2) + ". " + item.to_string())
        return items


class Track(object):
    chat_id = None

    def __init__(self, title="", duration="", file="", cover=""):
        self.title = title
        self.duration = duration
        self.file = file
        self.cover = cover

    def play(self):
        player.play(self.file)
        Announcer.now_playing(self)

    def to_string(self, elapsed=""):
        if elapsed != "":
            elapsed = utils.convert_duration(elapsed)

        if elapsed == "" and self.duration == "":
            return self.title
        if elapsed != "" and self.duration == "":
            return f"{self.title} [{elapsed}]"
        if elapsed == "" and self.duration != "":
            return f"{self.title} [{self.duration}]"
        return f"{self.title} [{elapsed} / {self.duration}]"


class Announcer(object):
    def now_playing(track):
        symbol = choice(["🎹", "🎙", "🎸", "🥁", "🎻", "🎺"])
        text = f"{symbol} Now playing:\n{track.to_string()}"
        logging.info(text.replace("\n", " "))
        keyboard = ("vol_down", "pause", "skip", "stop", "vol_up")
        send_msg(text, track.chat_id, pic=track.cover, keyboard=keyboard)

    def add_to_queue(track):
        send_msg(
            f"⭐ Added to queue: \n{track.to_string()}",
            track.chat_id,
            keyboard=("skip",),
        )


# --- Player callbacks ---


@player.event_callback("end-file")
def on_end_file(event):
    if event["event"]["reason"] != 2:  # if not skipped
        queue.skip()
    # TODO: catch errors


# --- Message handlers ---


@bot.message_handler(
    func=lambda message: settings.allowed_ids
    and message.from_user.id not in settings.allowed_ids
)
def unauthorized_msg(message):
    logging.info(f"Unauthorized access from {message.from_user.id}")
    bot.reply_to(
        message,
        f"⚠ You are not allowed to use this bot ⚠\nYour ID: {message.from_user.id}",
    )


@bot.message_handler(commands=["start"])
def start_msg(message):
    send_msg(commands.start_message, message.chat.id, keyboard=keyboards.main())


@bot.message_handler(commands=commands.volume_prefixes)
def volume_msg(message):
    inp = message.text
    id = message.chat.id
    volume = inp[inp.find(" ") + 1 :].lower()
    if volume[1:] in commands.volume_prefixes:  # message.text is "/v"
        volume = int(player.volume)
        if volume == 0:
            symbol = "🔇"
        else:
            symbol = "🔊"
        send_msg(f"{symbol} {volume}%", id, keyboard=("vol_down", "vol_up"))
        return
    if volume.startswith("-") or volume.startswith("+"):
        if volume.startswith("+"):
            volume = volume[1:]
        try:
            volume = int(volume)
        except:
            return
        volume = int(player.volume + volume)
    else:
        try:
            volume = int(volume)
        except:
            return
    if volume == 0:
        symbol = "🔇"
    else:
        symbol = "🔊"
    volume = max(min(volume, 100), 0)
    player.volume = volume
    send_msg(f"{symbol} {volume}%", id, keyboard=("vol_down", "vol_up"))


@bot.message_handler(commands=commands.skip_commands)
def skip_msg(message):
    id = message.chat.id
    if queue.len == 0:
        send_msg("Nothing playing! 💤", id)
    else:
        queue.skip()
        if queue.len == 0:
            send_msg("👌", id)


@bot.message_handler(commands=commands.stop_commands)
def stop_msg(message):
    id = message.chat.id
    if queue.len == 0:
        send_msg("Nothing playing! 💤", id)
    else:
        queue.stop()
        send_msg("⏹", id)


@bot.message_handler(commands=commands.pause_commands)
def pause_msg(message):
    id = message.chat.id
    state = player.pause
    if state == False:
        send_msg("⏸", id)
    else:
        send_msg("▶", id)
    player.pause = not (state)


@bot.message_handler(commands=commands.queue_commands)
def queue_msg(message):
    id = message.chat.id
    if queue.len == 0:
        send_msg("Nothing playing! 💤", id)
        return
    answer = "\n".join(queue.items())
    send_msg(answer, id, keyboard=("skip", "stop"))


@bot.message_handler(commands=commands.radio_prefixes)
def radio_msg(message):
    if not settings.radio:
        return
    inp = message.text
    id = message.chat.id
    symbol = choice(["🚀", "⌛", "🔍", "🔎", "🎲"])
    bot.reply_to(message, f"Searching... {symbol}")

    radio_title = " ".join(inp.split(" ")[1:])
    try:
        stantion = radio_provider.get(radio_title)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, str(e))
        return
    if stantion != ():
        track = Track(*stantion)
        track.chat_id = id
        queue.add(track)
    else:
        bot.reply_to(message, "Not found ⚠")


@bot.message_handler(commands=commands.lyrics_commands)
def lyrics_msg(message):
    if not settings.genius_token:
        return
    id = message.chat.id
    if queue.len == 0:
        send_msg("Nothing playing! 💤", id)
        return
    if queue.now.duration == "":  # radio
        return
    symbol = choice(["🚀", "⌛", "🔍", "🔎", "🎲"])
    bot.reply_to(message, f"Searching... {symbol}")

    try:
        lyrics = lyrics_provider.get(queue.now.title.split("(")[0].split("[")[0])
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, str(e))
        return
    if lyrics != {}:
        answer = f"📄 Lyrics for {lyrics['title']}:\n{lyrics['lyrics']}"
        send_msg(answer, id, pic=lyrics["art"])
    else:
        bot.reply_to(message, "Not found ⚠")


@bot.message_handler(func=lambda message: message.text)
def play_msg(message):
    id = message.chat.id
    if message.text.startswith("/"):
        send_msg("Unknown command ⚠", id)
        return
    track_title = message.text
    symbol = choice(["🚀", "⌛", "🔍", "🔎", "🎲"])
    bot.reply_to(message, f"Searching... {symbol}")

    try:
        tracks = music_provider.get(track_title)
        for track in tracks:
            if track == ():
                bot.reply_to(message, "Not found ⚠")
                continue
            track = Track(*track)
            track.chat_id = id
            queue.add(track)
    except Exception as e:
        logging.error(e)
        bot.reply_to(message, str(e))
        return


# --- Buttons handler ---


@bot.callback_query_handler(func=lambda call: True)
def buttton_callback(call):
    if call.data == "pause" or call.data == "play":
        is_paused = player.pause
        if not is_paused:
            bot.answer_callback_query(callback_query_id=call.id, text="⏸")
        else:
            bot.answer_callback_query(callback_query_id=call.id, text="▶")
        player.pause = not (is_paused)
    if call.data == "skip":
        if queue.len != 0:
            bot.answer_callback_query(callback_query_id=call.id, text="👌")
            queue.skip()
    if call.data == "stop":
        if queue.len != 0:
            bot.answer_callback_query(callback_query_id=call.id, text="⏹")
            queue.stop()
    if call.data == "vol_up":
        volume = min(player.volume + 10, 100)
        bot.answer_callback_query(callback_query_id=call.id, text=f"🔊 {int(volume)}%")
        player.volume = volume
    if call.data == "vol_down":
        volume = max(player.volume - 10, 0)
        if volume == 0:
            symbol = "🔇"
        else:
            symbol = "🔊"
        bot.answer_callback_query(
            callback_query_id=call.id, text=f"{symbol} {int(volume)}%"
        )
        player.volume = volume


queue = Queue()


def run():
    bot.infinity_polling()
