"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
skip_commands = ["s", "skip"]
stop_commands = ["stop"]
queue_commands = ["q", "queue"]
pause_commands = ["p", "pause"]
volume_prefixes = ["v", "volume"]
radio_prefixes = ["r", "radio"]
lyrics_commands = ["l", "lyrics"]

start_message = f"""Hello!
I am a bot that will play music for you. Search for music simply by sending a title or link to a YouTube video.
List of available commands:
/{skip_commands[0]} - Skip the currently playing song
/{stop_commands[0]} - Stop playback and clear the queue
/{queue_commands[0]} - Show current queue
/{pause_commands[0]} - Pause playback
/{volume_prefixes[0]} - Show current volume
/{volume_prefixes[0]} +10 - Change current volume
/{volume_prefixes[0]} 50 - Set volume
/{radio_prefixes[0]} - Search for radio
/{lyrics_commands[0]} - Search for lyrics

Source code: https://github.com/raitonoberu/realmusicbot
"""