"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from telebot import types
from .commands import *
import enum


def main():
    # Global keyboard
    keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    keyboard.add(
        f"/{volume_prefixes[1]} -10",
        f"/{pause_commands[1]}",
        f"/{skip_commands[1]}",
        f"/{volume_prefixes[1]} +10",
    )
    return keyboard


def create(args):
    keyboard = types.InlineKeyboardMarkup(row_width=len(args))
    bs = []
    for button in args:
        bs.append(buttons[button].value)
    keyboard.row(*bs)
    return keyboard


class buttons(enum.Enum):
    pause = types.InlineKeyboardButton(text="⏸", callback_data="pause")
    play = types.InlineKeyboardButton(text="▶️", callback_data="play")
    skip = types.InlineKeyboardButton(text="⏭", callback_data="skip")
    stop = types.InlineKeyboardButton(text="⏹️", callback_data="stop")
    vol_up = types.InlineKeyboardButton(text="🔊+", callback_data="vol_up")
    vol_down = types.InlineKeyboardButton(text="🔊-", callback_data="vol_down")
