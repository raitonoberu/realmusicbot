"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from setuptools.command.install import install
from setuptools import setup, find_packages
import subprocess
import os
import struct
import sys
import platform
import tempfile
import stat
import shutil

current_dir_path = os.path.dirname(os.path.realpath(__file__))
system = platform.system()


def prepare_linux():
    # create service
    create_service_script_path = os.path.join(
        current_dir_path, "realmusicbot", "install_scripts", "create_service.sh"
    )
    st = os.stat(create_service_script_path)
    os.chmod(create_service_script_path, st.st_mode | stat.S_IEXEC)
    subprocess.check_output([create_service_script_path])


def prepare_windows():
    # download mpv

    # 64bit or 32bit Python
    bit = 8 * struct.calcsize("P")
    if bit == 64:
        mpv_url = "https://downloads.sourceforge.net/project/mpv-player-windows/libmpv/mpv-dev-x86_64-20220731-git-284fecc.7z"
    if bit == 32:
        mpv_url = "https://downloads.sourceforge.net/project/mpv-player-windows/libmpv/mpv-dev-i686-20220731-git-284fecc.7z"

    # install 7zip unpacker 
    subprocess.check_output(
        [sys.executable, "-m", "pip", "install", "pyunpack", "patool", "requests"]
    )
    from pyunpack import Archive
    import requests

    with tempfile.TemporaryDirectory() as tdir:
        mpv_path = os.path.join(tdir, "mpv.7z")

        with open(mpv_path, "wb") as f:
            f.write(requests.get(mpv_url).content)

        Archive(mpv_path).extractall(tdir)
        lib_path = os.path.join(tdir, "mpv-2.dll")
        new_path = os.path.dirname(
            subprocess.check_output(["where", "realmusicbot"]).decode().strip()
        )
        shutil.copy2(lib_path, os.path.join(new_path, "mpv-2.dll"))


class InstallService(install):
    def run(self):
        install.run(self)
        if system == "Linux":
            prepare_linux()
            home = os.getenv("HOME")
        if system == "Windows":
            prepare_windows()
            home = os.getenv("USERPROFILE")

        settings_to = os.path.join(home, ".config", "realmusicbot.ini")
        settings_from = os.path.join(current_dir_path, "realmusicbot", "settings.ini")
        if not (os.path.exists(settings_to)):
            os.makedirs(os.path.dirname(settings_to), exist_ok=True)
            shutil.copy2(settings_from, settings_to)


setup(
    name="realmusicbot",
    version="2.1",
    author="raitonoberu",
    description="Play music from YouTube and control playback with Telegram",
    author_email="raitonoberu@mail.ru",
    url="https://github.com/raitonoberu/realmusicbot",
    packages=find_packages(),
    entry_points={"console_scripts": ["realmusicbot = realmusicbot:run"]},
    install_requires=[
        "python-mpv",
        "pyradios",
        "pyTelegramBotAPI",
        "ytmusicapi",
        "yt-dlp",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: No Input/Output (Daemon)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    cmdclass={"install": InstallService},
)
