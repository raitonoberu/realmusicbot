import pafy
from youtube_search import YoutubeSearch


def get_url(name_or_url):
    if "youtu" in name_or_url:  # detect youtube link
        return name_or_url
    results = YoutubeSearch(name_or_url, max_results=1).to_dict()
    for i in range(2):  # try 2 times to avoid network issues
        if results != []:
            break
        results = YoutubeSearch(name_or_url, max_results=1).to_dict()
    if results != []:
        return f"https://www.youtube.com{results[0]['link']}"
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
