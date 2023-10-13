"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from .settings import itag
from .utils import convert_duration
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
import re

ytmusic = YTMusic()

videoId_regex = re.compile(r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)")
playlistId_regex = re.compile(r"(?<=list=)([\w-]+)")


def get(name_or_url):
    if "youtu" in name_or_url:  # detect youtube link
        if "playlist" in name_or_url:
            # TODO: decide what to do with playlists
            yield from _get_playlist(name_or_url)
            return
        regex = videoId_regex.findall(name_or_url)
        if len(regex) == 0 or len(regex[0]) < 4:
            yield ()
            return
        yield _get_video(regex[0][3], itag)
    else:
        result = ytmusic.search(name_or_url, filter="songs", limit=1)
        if not result:
            yield ()
            return
        yield (
            _get_title(result[0]),
            *_get_video(result[0].get("videoId", ""), itag)[1:],
        )


def _get_playlist(url):
    regex = playlistId_regex.findall(url)
    if len(regex) == 0:
        yield ()
        return
    playlistId = regex[0]

    playlist = ytmusic.get_playlist(playlistId)
    for track in playlist.get("tracks", []):
        try:
            yield (
                _get_title(track),
                *_get_video(track.get("videoId", ""), itag)[1:],
            )
        except Exception as e:
            print(e)


def _get_video(video_id, itag):
    url = f"https://www.youtube.com/watch?v={video_id}"
    info = {}
    with YoutubeDL(params={"quiet": True, "format": str(itag)}) as ydl:
        info = ydl.extract_info(url, download=False)

    author = info.get("uploader", "")
    if " - Topic" in author:
        title = author.replace(" - Topic", "") + " - " + info.get("title", "")
    else:
        title = info.get("title", "")

    duration = convert_duration(info.get("duration", 0))
    stream = info.get("url", "")

    return title, duration, stream, url


def _get_title(track):
    artist = ""
    for i, a in enumerate(track.get("artists", [])):
        if i != 0:
            artist += ", "
        artist += a.get("name", "")

    title = track.get("title", "")

    if artist != "":
        return artist + " - " + title
    return title
