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
            current_dir_path, 'realmusicbot', 'install_scripts', 'create_service.sh')
        st = os.stat(create_service_script_path)
        os.chmod(create_service_script_path, st.st_mode | stat.S_IEXEC)
        subprocess.check_output([create_service_script_path])
        new_settings = current_dir_path + "/realmusicbot/realmusicbot_settings.py"
        settings = os.getenv("HOME") + "/realmusicbot_settings.py"
        if not(os.path.isfile(settings)):
            # create new settings
            shutil.copy2(new_settings, settings)
        else:
            # do not touch settings
            shutil.copy2(new_settings, settings + ".new")


setup(
    name='realmusicbot',
    version='1.0',
    author='raitonoberu',
    description='Control your Music Player Daemon with Telegram and play music from YouTube',
    author_email='disith@mail.ru',
    url='https://github.com/raitonoberu/realmusicbot',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'realmusicbot = realmusicbot.__main__:main'
        ]
    },
    install_requires=[
        'lyricsgenius>=1.8.6',
        'youtube_search>=0.1.3',
        'youtube_dl>=2020.6.6',
        'pyradios>=0.0.21',
        'python_mpd2>=1.0.0',
        'pyTelegramBotAPI>=3.7.1',
        'pafy @ git+https://github.com/mps-youtube/pafy',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: Apache Software License'
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.7',
    cmdclass={'install': InstallService}
)
