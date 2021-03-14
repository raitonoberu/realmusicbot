"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from pyradios import RadioBrowser

rb = RadioBrowser()


def get(radio_title):
    stantions = rb.stations_by_name(radio_title)
    if stantions == []:
        return ()
    stantion = sorted(stantions, key=lambda k: k["votes"], reverse=True)[0]
    return (stantion["name"], "", stantion["url_resolved"], stantion.get("favicon"))
