"""
RealMusicBot: Control your speakers with Telegram and play music from YouTube
Copyright (C) 2021  raitonoberu
"""
from setuptools.command.install import install
from setuptools import setup, find_packages
import subprocess
import os
import stat
import shutil


class InstallService(install):
    def run(self):
        install.run(self)
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        create_service_script_path = os.path.join(
            current_dir_path, "realmusicbot", "install_scripts", "create_service.sh"
        )
        st = os.stat(create_service_script_path)
        os.chmod(create_service_script_path, st.st_mode | stat.S_IEXEC)
        subprocess.check_output([create_service_script_path])
        new_settings = current_dir_path + "/realmusicbot/settings.ini"
        settings = os.getenv("HOME") + "/.config/realmusicbot.ini"
        if not (os.path.exists(settings)):
            shutil.copy2(new_settings, settings)


setup(
    name="realmusicbot",
    version="2.0",
    author="raitonoberu",
    description="Play music from YouTube and control playback with Telegram",
    author_email="raitonoberu@mail.ru",
    url="https://github.com/raitonoberu/realmusicbot",
    packages=find_packages(),
    entry_points={"console_scripts": ["realmusicbot = realmusicbot:run"]},
    install_requires=[
        "python-mpv",
        "lyricsgenius",
        "youtube-search-python",
        "pyradios",
        "pyTelegramBotAPI",
        "pytube",
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
