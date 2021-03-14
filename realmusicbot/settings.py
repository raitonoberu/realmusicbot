"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from configparser import ConfigParser
import os

_path = os.getenv("HOME") + "/.config/realmusicbot.ini"
if not os.path.exists(_path):
    print("Can't find the config file! Copying...")
    from shutil import copyfile

    copyfile("settings.ini", _path)
    print("- Please, fill the config file located at " + _path)
    raise NotImplementedError()
config = ConfigParser(allow_no_value=True)
config.read(_path)


token = config.get("SETTINGS", "TOKEN")
threaded = config.get("SETTINGS", "THREADED")
itag = config.getint("SETTINGS", "ITAG")
language = config.get("SETTINGS", "LANGUAGE")
radio = config.getboolean("SETTINGS", "RADIO")
genius_token = config.get("SETTINGS", "GENIUS_TOKEN")
allowed_ids = [
    int(i) for i in config.get("SETTINGS", "ALLOWED_IDS").split(",") if i != ""
]
