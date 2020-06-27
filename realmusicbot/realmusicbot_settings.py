# -----CONFIGURATION-----
LOGGING = False
LOG_FILE = "realmusicbot.log"

THREADED = False
# (buggy, not recommended)

# Get your token using tg @BotFather
# https://t.me/botfather
TOKEN = "<ENTER YOUR BOT TOKEN HERE>"

MPD_IP = "localhost"
MPD_PORT = "6600"

# -----CUSTOMIZATION-----

# 1. Enable global keyboard
KEYBOARD = True

# 2. Allows you to search radio (/radio <stantion>)
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


volume_prefixes = ["v", "volume"]
skip_commands = ["s", "skip"]
queue_commands = ["q", "queue"]
stop_commands = ["stop"]
pause_commands = ["p", "pause"]
radio_prefixes = ["r", "radio"]
lyrics_commands = ["l", "lyrics"]
