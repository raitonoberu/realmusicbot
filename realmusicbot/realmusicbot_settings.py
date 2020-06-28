# -----CONFIGURATION-----
LOGGING = False
LOG_FILE = "realmusicbot.log"

THREADED = False  # (buggy, not recommended)

TIMEOUT = 5  # Requests read timeout (secs)

# Get your token using tg @BotFather
# https://t.me/botfather
TOKEN = "<ENTER YOUR BOT TOKEN HERE>"

MPD_IP = "localhost"
MPD_PORT = "6600"

# -----CUSTOMIZATION-----

# 1. Enable global keyboard
KEYBOARD = True

# 2. Allows you to search radio (/radio <station>)
RADIO_ON = True

# 3. Allows you to search lyrics (/lyrics)
# - Get your Genius API Token here:
# - https://genius.com/api-clients
GENIUS_TOKEN = ""

# 4. Bot privatization (HIGHLY RECOMMENDED)
# - Get your User ID using tg @userinfobot and add it to the list
# - https://t.me/userinfobot
# - If you leave it empty, everyone can use the bot
ALLOWED_IDS = []  # example: [123456789, 987641234]

skip_commands = ["s", "skip"]
stop_commands = ["stop"]
queue_commands = ["q", "queue"]
pause_commands = ["p", "pause"]
volume_prefixes = ["v", "volume"]
radio_prefixes = ["r", "radio"]
lyrics_commands = ["l", "lyrics"]

START_MESSAGE = f"""Hello!
I am a bot that will play music for you. Search for music simply by sending a title or link to a YouTube video.
List of available commands:
/{skip_commands[0]} - Skips the currently playing song
/{stop_commands[0]} - Stops playback and clears the queue
/{queue_commands[0]} - Shows current queue
/{pause_commands[0]} - Pauses playback
/{volume_prefixes[0]} - Shows current volume
/{volume_prefixes[0]} +10 - Changes current volume
/{volume_prefixes[0]} 50 - Sets volume
/{radio_prefixes[0]} - Searches for radio
/{lyrics_commands[0]} - Searches for lyrics

Source code: https://github.com/raitonoberu/realmusicbot
"""
