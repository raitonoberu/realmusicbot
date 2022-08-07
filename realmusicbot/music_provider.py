"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from .settings import itag
from .utils import convert_duration
from ytmusicapi import YTMusic
import requests
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
        videoId = regex[0][3]
    else:
        result = ytmusic.search(name_or_url, filter="songs", limit=1)
        if not result:
            yield ()
            return
        videoId = result[0]["videoId"]
    yield _get_video(videoId, itag)


def _get_playlist(url):
    regex = playlistId_regex.findall(url)
    if len(regex) == 0:
        yield ()
        return
    playlistId = regex[0]

    playlist = ytmusic.get_playlist(playlistId)
    for track in playlist["tracks"]:
        videoId = track["videoId"]
        try:
            yield _get_video(videoId, itag)
        except Exception as e:
            print(e)


def _get_video(video_id, itag):
    player = requests.post(
        "https://www.youtube.com/youtubei/v1/player",
        json={
            "context": {
                "client": {
                    "clientName": "ANDROID",
                    "clientScreen": "EMBED",
                    "clientVersion": "16.43.34",
                },
                "thirdParty": {
                    "embedUrl": "https://www.youtube.com",
                },
            },
            "videoId": video_id,
        },
        headers={"X-Goog-Api-Key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"},
    ).json()

    author = player["videoDetails"]["author"]
    if " - Topic" in author:
        title = author.replace(" - Topic", "") + " - " + player["videoDetails"]["title"]
    else:
        title = player["videoDetails"]["title"]
    duration = convert_duration(player["videoDetails"]["lengthSeconds"])
    stream = ""
    formats = player["streamingData"]["adaptiveFormats"]
    for f in formats:
        if f["itag"] == itag:
            stream = f["url"]
            break
    url = f"https://www.youtube.com/watch?v={video_id}"

    return title, duration, stream, url
