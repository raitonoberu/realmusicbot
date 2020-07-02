import pafy
from youtubesearchpython import searchYoutube
#  A BIG THANKS to https://github.com/alexmercerind


def get_url(name_or_url):
    if "youtu" in name_or_url:  # detect youtube link
        return name_or_url
    result = searchYoutube(name_or_url, mode="list").result()
    if result:
        return result[0][2]
    else:
        return ""


def get_playlist(url):
    playlist = pafy.get_playlist(url)
    for video in playlist['items']:
        video = video['pafy']
        try:
            video = {
                "title": video.title,
                "duration": video.length,
                "file": video.getbestaudio().url,
                "cover": video.watchv_url}
            yield video
        except Exception as e:
            print(e)
            pass


def get(name_or_url):
    url = get_url(name_or_url)
    if url == "":
        yield {}
        return
    if "playlist" in url:
        yield from get_playlist(url)
        return
    video = pafy.new(url)
    yield {"title": video.title,
           "duration": video.length,
           "file": video.getbestaudio().url,
           "cover": video.watchv_url}
