"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""


def convert_duration(time):
    """Convert seconds to HH:MM:SS"""
    time = int(time)
    hours = time // 3600
    mins = time % 3600 // 60
    secs = time % 60
    if len(str(hours)) == 1 and hours != 0:
        hours = f"0{hours}"
    if len(str(mins)) == 1:
        mins = f"0{mins}"
    if len(str(secs)) == 1:
        secs = f"0{secs}"
    if hours == 0:
        return f"{mins}:{secs}"
    else:
        return f"{hours}:{mins}:{secs}"