"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from configparser import ConfigParser
import platform
import os

_system = platform.system()
if _system == "Windows":
    _home = os.getenv("USERPROFILE")
else:
    _home = os.getenv("HOME")

_path = os.path.join(_home, ".config", "realmusicbot.ini")

if not os.path.exists(_path):
    raise NotImplementedError("Can't find the config file! Path: " + _path)

config = ConfigParser(allow_no_value=True)
config.read(_path)

token = config.get("SETTINGS", "TOKEN")
if not token or token == "yourtoken":
    raise NotImplementedError("Please, fill the config file located at " + _path)
threaded = config.get("SETTINGS", "THREADED")
itag = config.getint("SETTINGS", "ITAG")
language = config.get("SETTINGS", "LANGUAGE")
allowed_ids = [
    int(i) for i in config.get("SETTINGS", "ALLOWED_IDS").split(",") if i != ""
]
