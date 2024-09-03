import os
import yt_dlp

import main

if main.useCustomFFMPEG:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'ffmpeg_location': main.ffmpegRoute,
        'outtmpl': os.path.join(os.getcwd(), './Downloads', '%(title)s.%(ext)s'),
        'nooverwrites': True,
        'restrictfilenames': True
    }
else:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(os.getcwd(), './Downloads', '%(title)s.%(ext)s'),
        'nooverwrites': True,
        'restrictfilenames': True
    }


def download_song(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url)
        title = info_dict.get('title', None)
        channel = info_dict.get('uploader', None)
        duration = info_dict.get('duration', None)
        filesize = info_dict.get('filesize', None)
        artist = info_dict.get('artist')
        thumbnail = info_dict.get('thumbnail', None)
        n_file = info_dict['requested_downloads'][0]['filepath']
        ydl.download([url])

    return title, channel, duration, filesize, artist, thumbnail, n_file
