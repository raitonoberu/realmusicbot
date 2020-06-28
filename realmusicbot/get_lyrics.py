import lyricsgenius
from .settings import GENIUS_TOKEN


def get_lyrics(title):
    genius = lyricsgenius.Genius(GENIUS_TOKEN)
    genius.verbose = False
    song = genius.search_song(title, get_full_info=False)
    if song is None:
        return {}

    return {"title": f"{song.artist} - {song.title}",
            "lyrics": song.lyrics,
            "art": song.song_art_image_url}
