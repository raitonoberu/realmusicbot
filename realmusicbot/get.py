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


def get(name_or_url):
    url = get_url(name_or_url)
    if url == "":
        return {}
    video = pafy.new(url)
    cover = video.getbestthumb()
    return {"title": video.title,
            "duration": video.length,
            "file": video.getbestaudio().url,
            "cover": url}
