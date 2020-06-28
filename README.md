<h1 align="center">🎶 Real Music Bot (beta) 🎶</h1>

<p align="center">
    Control your speakers with Telegram and play music from YouTube
</p>

<img src="screenshots/searching2.png?raw=true" width="200" />

## What is it?

If you've ever used Discord, you've probably heard of music bots that play music for you. All you had to do was just type "**-p \<track_name\>**" to listen to your favorite song. I also liked it, so I made the real one!<br>
This is a kind of addition to the awesome [Music Player Daemon](https://github.com/MusicPlayerDaemon/MPD). This script runs as a service on Raspberry Pi and allows you to play music from YouTube and control playback using Telegram.

## Features

- #### Search for music simply by sending a title...
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/searching.png?raw=true" width="300"/>
</details>
- #### ...or link to a YouTube video
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/yt.png?raw=true" width="300"/>
</details>
- #### Use the search provided by @vid bot
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/vid.png?raw=true" width="300"/>
</details>
- #### Fully working queue
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/queue.png?raw=true" width="300"/>
</details>
- #### Turn on your favorite radio
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/radio.png?raw=true" width="300"/>
</details>
- #### Search for song lyrics
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/lyrics.png?raw=true" width="300"/>
</details>
- #### Protect the bot from unauthorized users
<details>
    <summary>Screenshot</summary>
    <img src="screenshots/privatization.png?raw=true" width="300"/>
</details>

List of available commands:

- **/s** - Skips the currently playing song
- **/stop** - Stops playback and clears the queue
- **/q** - Shows current queue
- **/p** - Pauses playback
- **/v** - Shows current volume
- **/v +10** - Changes current volume
- **/v 50** - Sets volume
- **/r** <station> - Searches for radio
- **/l** - Searches for lyrics


## Installation (Raspberry Pi / Linux)

Make sure you have [Python 3.7+ installed](https://www.python.org/downloads/)

### 1. Install packages

    $ sudo apt install mpd
    $ git clone https://github.com/raitonoberu/realmusicbot
    $ pip3 install ./realmusicbot


### 2. Change settings

Before running, you must configure your bot by editing the file **~/realmusicbot_settings.py**:

    $ nano ~/realmusicbot_settings.py

#### 2.1 Set your bot token

[How do I create a bot?](https://core.telegram.org/bots#6-botfather)

    TOKEN = "<ENTER YOUR BOT TOKEN HERE>"

#### 2.2 Enable additional features (optional)

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

### 3. Run your bot

Start MPD first:

    $ sudo systemctl start mpd
    $ sudo systemctl enable mpd

There are two ways to run Real Music Bot. It's recommended to run it in a terminal first to make sure that it works.

#### 3.1 Running in a terminal

    $ realmusicbot

Press **Ctrl+C** to close.

#### 3.2 Running as a service

    $ systemctl --user start realmusicbot
    $ systemctl --user enable realmusicbot

Check logs:

    $ journalctl | grep realmusicbot

## Uninstallation

    $ systemctl --user stop realmusicbot
    $ systemctl --user disable realmusicbot
    $ sudo rm ~/.config/systemd/user/realmusicbot.service
    $ sudo rm -r ~/realmusicbot*
    $ pip3 uninstall realmusicbot

## Credits

Max Kellermann (MaxKellermann) for [Music Player Daemon](https://github.com/MusicPlayerDaemon/MPD)

FrankWang (eternnoir) for [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

André P. Santos (andreztz) for [pyradios](https://github.com/andreztz/pyradios)

John W. Miller (johnwmillr) for [LyricsGenius](https://github.com/johnwmillr/LyricsGenius)

"mps-youtube" organization for [Pafy](https://github.com/mps-youtube/pafy)

joe tats (joetats) for [youtube_search](https://github.com/joetats/youtube_search)
