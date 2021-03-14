<h1 align="center">🎶 Real Music Bot 2.0 🎶</h1>

<p align="center">
    Control your speakers with Telegram and play music from YouTube

<img src="screenshots/searching2.png?raw=true" width="200" />
</p>

## What is it?

If you've ever used Discord, you've probably heard of music bots that play music for you. All you had to do was just type "**-p \<track_name\>**" to listen to your favorite song. I also liked it, so I made the real one!<br>
This script runs as a service and allows you to play music from YouTube and control playback using Telegram. It uses an awesome [MPV](https://github.com/mpv-player/mpv) media player as a backend.

## Features

- ### Search for music simply by sending a title...

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/searching.png?raw=true" width="300"/>
</details>

- ### ...or link to a YouTube video

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/yt.png?raw=true" width="300"/>
</details>

- ### Use the search provided by @vid bot

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/vid.png?raw=true" width="300"/>
</details>

- ### Fully working queue

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/queue.png?raw=true" width="300"/>
</details>

- ### Turn on your favorite radio

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/radio.png?raw=true" width="300"/>
</details>

- ### Search for song lyrics

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/lyrics.png?raw=true" width="300"/>
</details>

- ### Protect the bot from unauthorized users

<details>
    <summary>Screenshot</summary>
    <img src="screenshots/privatization.png?raw=true" width="300"/>
</details>

List of available commands:

- **/s** - Skip the currently playing song
- **/stop** - Stop playback and clear the queue
- **/q** - Show current queue
- **/p** - Pause playback
- **/v** - Show current volume
- **/v +10** - Change current volume
- **/v 50** - Set volume
- **/r** <station> - Search for radio
- **/l** - Search for lyrics


## Installation (Raspberry Pi / Linux)

Make sure you have [Python 3.7+ installed](https://www.python.org/downloads/)

### 1. Install packages

    $ sudo apt install mpv
    $ pip3 install https://github.com/raitonoberu/realmusicbot/archive/master.zip


### 2. Change settings

Before running, you must configure your bot by editing the file **~/.config/realmusicbot.ini**:

    $ nano ~/.config/realmusicbot.ini

#### 2.1 Set your bot token

[How do I create a bot?](https://core.telegram.org/bots#6-botfather)

    TOKEN=yourtoken

#### 2.2 Configure additional features (optional)

    # Whether to process messages simultaneously
    THREADED=true

    # Select YouTube ITAG code
    # - 251 is the highest quality
    # - More here: https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2
    ITAG=251

    # Allows you to search radio (/radio <station>)
    RADIO=true

    # Allows you to search lyrics (/lyrics)
    # - Get your Genius Client Access Token here:
    # - https://genius.com/api-clients
    GENIUS_TOKEN=

    # Bot privatization (HIGHLY RECOMMENDED)
    # - Get your User ID using tg @userinfobot and add it to the list
    # - https://t.me/userinfobot
    # - If you leave it empty, everyone can use the bot
    # - example: 123456789,987641234
    ALLOWED_IDS=

### 3. Run your bot

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
    $ sudo rm -r ~/.config/realmusicbot.ini
    $ pip3 uninstall realmusicbot

## Credits

"mpv-player" organization for [mpv](https://github.com/mpv-player/mpv)

FrankWang (eternnoir) for [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

André P. Santos (andreztz) for [pyradios](https://github.com/andreztz/pyradios)

John W. Miller (johnwmillr) for [LyricsGenius](https://github.com/johnwmillr/LyricsGenius)

"pytube" organization for [Pafy](https://github.com/pytube/pytube)

Hitesh Kumar Saini (alexmercerind) for [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)

jaseg for [python-mpv](https://github.com/jaseg/python-mpv)

## License

GPLv3, see [LICENSE](./LICENSE) for additional info.

## TODO

* Localization
* Better exceptions handling & logging
* Passing params to MPV
* Running the bot in Windows