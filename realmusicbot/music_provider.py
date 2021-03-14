"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from .settings import itag
from .utils import convert_duration
from youtubesearchpython import VideosSearch, StreamURLFetcher, Video, Playlist

fetcher = StreamURLFetcher()

def _get_playlist(url):
    playlist = Playlist.getVideos(url)
    for video in playlist["videos"]:
        url = video["link"]
        try:
            duration = video["duration"]
            video = Video.get(url)
            stream = fetcher.get(video, itag)
            yield (video["title"], duration, stream, url)
        except Exception as e:
            print(e)


def get(name_or_url):
    if "youtu" in name_or_url:  # detect youtube link
        url = name_or_url
        if "playlist" in url:
            yield from _get_playlist(url)
            return
    else:
        result = VideosSearch(name_or_url, limit=1).result()["result"]
        if not result:
            yield ()
            return
        url = result[0]["link"]
        print(url)
    fetcher = StreamURLFetcher()
    video = Video.get(url)
    stream = fetcher.get(video, itag)
    duration = convert_duration(
        int(float(video["streamingData"]["formats"][0]["approxDurationMs"]) // 1000)
    )
    yield (video["title"], duration, stream, url)
