"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
import requests

API_URL = "https://lyricsapi.vercel.app/api/lyrics"


def get(title):
    lyrics = requests.get(API_URL, params={"name": title}).json()
    return "\n".join(line["words"] for line in lyrics).replace("♪", "")
