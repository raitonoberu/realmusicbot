from .settings import *
import telebot
telebot.apihelper.READ_TIMEOUT = TIMEOUT
import mpd

from time import sleep
from random import choice
from threading import Thread

from .get import get
from .keyboards import keyboards
if RADIO_ON:
    from .get_radio import get_radio
if GENIUS_TOKEN:
    from .get_lyrics import get_lyrics

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(funcName)s) %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ] if LOGGING else [logging.StreamHandler()]
)


bot = telebot.TeleBot(TOKEN, threaded=THREADED)


def player():
    """Track announcement thread"""
    announce = True
    refresh_rate = 0.5
    while True:
        sleep(refresh_rate)
        global queue
        if queue == []:  # nothing is playing
            announce = True
            continue
        track = whatisplaying()
        if track == {}:  # last track is over
            announce = True
            queue = []
            continue
        try:
            if track.get("file") == queue[0]['file']:
                s = status()
                if announce:
                    symbol = choice(
                        ['🎹', '🎙', '🎸', '🥁', '🎻', '🎺'])
                    text = f"{symbol} Now playing:\n{queue[0]['title']} [{queue[0]['duration']}]"
                    logging.info(text.replace("\n", " "))
                    keyboard = ("vol_down", "pause", "skip", "stop", "vol_up")
                    send_msg(text, queue[0]['id'], pic=queue[0]
                              ['cover'], keyboard=keyboard)
                    announce = False
                if s.get('error'):
                    send_msg(
                        f"Error! ⚠\n{s['error']}", queue[0]['id'])
                    play()
                    skip()
                    queue.pop(0)
                    announce = True
            elif len(queue) > 1:
                announce = True
                # next track is playing
                if track['file'].strip() == queue[1]['file'].strip():
                    queue.pop(0)
                else:  # nobody knows what is playing *_*
                    logging.error(
                        f"Unknown track\nqueue[0]: {queue[0]}\nplaying: {track['file']}")
        except:
            logging.exception('')


def add(dictionary, id, announce=True):
    """Add track to MPD"""
    try:
        client.add(dictionary['file'])
        if whatisplaying() == {} or whatisplaying().get('file') == dictionary['file']:
            play()
        elif announce:
            send_msg(
                f"⭐ Added to queue: \n{dictionary['title']} [{dictionary['duration']}]", id, keyboard=("skip",))
        dictionary['id'] = id
        queue.append(dictionary)
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        add(dictionary, id, announce=announce)


def duration(time):
    """Convert seconds to HH:MM:SS"""
    time = int(time)
    hours = time // 3600
    mins = time % 3600 // 60
    secs = time % 60
    if len(str(hours)) == 1 and hours != 0:
        hours = f"0{hours}"
    if len(str(mins)) == 1:
        mins = f"0{mins}"
    if len(str(secs)) == 1:
        secs = f"0{secs}"
    if hours == 0:
        return f"{mins}:{secs}"
    else:
        return f"{hours}:{mins}:{secs}"


def whatisplaying():
    try:
        return client.currentsong()
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        return whatisplaying()


def play():
    try:
        client.play()
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        play()


def skip():
    try:
        client.next()
    except mpd.base.CommandError:  # nothing is playing
        pass
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        skip()


def stop():
    try:
        global queue
        queue = []
        client.stop()
        client.clear()
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        stop()


def pause():
    try:
        client.pause()
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        pause()


def set_volume(volume):
    try:
        client.setvol(volume)
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        set_volume(volume)


def add_volume(vol_change):
    try:
        volume = status()['volume']
        volume = int(volume) + vol_change
        if volume > 100:
            volume = 100
        if volume < 0:
            volume = 0
        set_volume(volume)
        return volume
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        return add_volume(vol_change)


def status():
    try:
        return client.status()
    except Exception as e:
        logging.info(e)
        sleep(1)
        connect()
        return status()


@bot.message_handler(func=lambda message: ALLOWED_IDS and message.from_user.id not in ALLOWED_IDS)
def unauthorized_msg(message):
    logging.info(f"Unauthorized access from {message.from_user.id}")
    bot.reply_to(
        message, f"⚠ You are not allowed to use this bot ⚠\nYour ID: {message.from_user.id}")

@bot.message_handler(commands=['start'])
def start_msg(message):
    send_msg(START_MESSAGE, message.chat.id)


@bot.message_handler(commands=volume_prefixes)
def volume_msg(message):
    inp = message.text
    id = message.chat.id
    volume = inp[inp.find(" ") + 1:].lower()
    if volume[1:] in volume_prefixes:  # message.text is "/v"
        volume = status()['volume']
        if volume == 0:
            symbol = '🔇'
        else:
            symbol = '🔊'
        send_msg(f"{symbol} {volume}%", id, keyboard=("vol_down", "vol_up"))
        return
    if volume.startswith('-') or volume.startswith('+'):
        if volume.startswith('+'):
            volume = volume[1:]
        try:
            volume = int(volume)
        except:
            return
        volume = add_volume(volume)
        if volume == 0:
            symbol = '🔇'
        else:
            symbol = '🔊'
        send_msg(f"{symbol} {volume}%", id, keyboard=("vol_down", "vol_up"))
        return
    try:
        volume = int(volume)
    except:
        volume = 101
    if volume < 101:
        if volume == 0:
            symbol = '🔇'
        else:
            symbol = '🔊'
        set_volume(volume)
        send_msg(f"{symbol} {volume}%", id, keyboard=("vol_down", "vol_up"))


@bot.message_handler(commands=skip_commands)
def skip_msg(message):
    id = message.chat.id
    state = status()['state']
    if state == "stop":
        send_msg("Nothing is playing! 💤", id)
    else:
        skip()
        send_msg("👌", id)


@bot.message_handler(commands=stop_commands)
def stop_msg(message):
    id = message.chat.id
    state = status()['state']
    if state == "stop":
        send_msg("Nothing is playing! 💤", id)
    else:
        stop()
        send_msg("⏹", id)


@bot.message_handler(commands=pause_commands)
def pause_msg(message):
    id = message.chat.id
    state = status()['state']
    if state == "play":
        send_msg("⏸", id)
    elif state == "pause":
        send_msg("▶", id)
    else:
        send_msg("Nothing is playing! 💤", id)
    pause()


@bot.message_handler(commands=queue_commands)
def queue_msg(message):
    id = message.chat.id
    if queue == []:
        send_msg("Nothing is playing! 💤", id)
        return
    s = status()
    if s['state'] == "pause":
        state = "⏸ Paused"
    else:
        state = "🎶 Now playing"
    elapsed = s.get('elapsed', "0")
    answer = [
        f"{state}: {queue[0]['title']} [{duration(float(elapsed))} / {queue[0]['duration']}]\n"]
    answer.extend([
        f"{i + 1}. {queue[i]['title']} [{queue[i]['duration']}]" for i in range(1, len(queue))])
    answer = "\n".join(answer)
    send_msg(answer, id, keyboard=("skip", "stop"))


@bot.message_handler(commands=radio_prefixes)
def radio_msg(message):
    if not RADIO_ON:
        return
    inp = message.text
    id = message.chat.id
    symbol = choice(['🚀', '⌛', '🔍', '🔎', '🎲'])
    bot.reply_to(message, f"Searching... {symbol}")
    radio_title = " ".join(inp.split(" ")[1:])
    try:
        stantion = get_radio(radio_title)
    except Exception as e:
        logging.error(e)
        stantion = {}
    if stantion != {}:
        add(stantion, id)
    else:
        send_msg("Not found ⚠", id)


@bot.message_handler(commands=lyrics_commands)
def lyrics_msg(message):
    if not GENIUS_TOKEN:
        return
    id = message.chat.id
    if len(queue) == 0:
        send_msg("Nothing is playing! 💤", id)
        return
    if queue[0]['duration'] == "radio":
        return
    symbol = choice(['🚀', '⌛', '🔍', '🔎', '🎲'])
    bot.reply_to(message, f"Searching... {symbol}")
    try:
        lyrics = get_lyrics(queue[0]['title'].split('(')[0]].split('[')[0])
    except Exception as e:
        logging.error(e)
        lyrics = {}
    if lyrics != {}:
        answer = f"📄 Lyrics for {lyrics['title']}:\n{lyrics['lyrics']}"
        send_msg(answer, id, pic=lyrics['art'])
    else:
        send_msg("Not found ⚠", id)


@bot.message_handler(func=lambda message: message.text)
def play_msg(message):
    id = message.chat.id
    if message.text.startswith('/'):
        send_msg("Unknown command ⚠", id)
        return
    track_title = message.text
    symbol = choice(['🚀', '⌛', '🔍', '🔎', '🎲'])
    bot.reply_to(message, f"Searching... {symbol}")
    try:
        link = get(track_title)
    except Exception as e:
        logging.error(e)
        link = {}
    if link != {}:
        link['duration'] = duration(link['duration'])
        add(link, id)
    else:
        send_msg("Not found ⚠", id)


@bot.callback_query_handler(func=lambda call: True)
def buttton_callback(call):
    state = status()['state']
    if call.data == "pause" or call.data == "play":
        if state == "play":
            bot.answer_callback_query(callback_query_id=call.id, text="⏸")
        elif state == "pause":
            bot.answer_callback_query(callback_query_id=call.id, text="▶")
        pause()
    if call.data == "skip":
        if state != "stop":
            bot.answer_callback_query(callback_query_id=call.id, text="👌")
            skip()
    if call.data == "stop":
        if state != "stop":
            bot.answer_callback_query(callback_query_id=call.id, text="⏹")
            stop()
    if call.data == "vol_up":
        volume = add_volume(10)
        bot.answer_callback_query(
            callback_query_id=call.id, text=f"🔊 {volume}%")
    if call.data == "vol_down":
        volume = add_volume(-10)
        if volume == 0:
            symbol = '🔇'
        else:
            symbol = '🔊'
        bot.answer_callback_query(
            callback_query_id=call.id, text=f"{symbol} {volume}%")


def connect():
    try:
        client.connect(MPD_IP, MPD_PORT)
        logging.info("Successfully connected to MPD")
    except Exception as e:
        if str(e) != "Already connected":
            logging.error(e)
            sleep(1)
            connect()


def send_msg(text, id, pic=None, keyboard=None):
    global KEYBOARD
    if KEYBOARD and keyboard is None:
        keyboard = keyboards.main()  # show global keyboard
        KEYBOARD = False
    elif isinstance(keyboard, tuple):  # custom inline keyboard
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


def main():
    global queue
    global client
    queue = []
    client = mpd.MPDClient()
    connect()
    stop()
    client.consume(1)
    client.replay_gain_mode('track')
    t = Thread(target=player, daemon=True)
    t.start()
    logging.info("Server has started")
    bot.infinity_polling(none_stop=True)


if __name__ == "__main__":
    main()
