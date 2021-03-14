"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
import lyricsgenius
from .settings import genius_token


def get(title):
    genius = lyricsgenius.Genius(genius_token)
    genius.verbose = False
    song = genius.search_song(title, get_full_info=False)
    if song is None:
        return {}

    return {
        "title": f"{song.artist} - {song.title}",
        "lyrics": song.lyrics,
        "art": song.song_art_image_url,
    }
