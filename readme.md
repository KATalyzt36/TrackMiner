# Track Miner

![Track Miner Logo](https://media.discordapp.net/attachments/1039680545858269246/1089243922779361320/KATalyzt_A_cat_with_a_phosphorescent_moon_on_its_forehead_which_08f63728-a5e3-462c-bdc2-a9a012d87e82.png?width=442&height=442 "Track Miner Logo")

## Usage:

- You just need to send a YouTube link. Keep in mind that if the video is very long or heavy, there may be some error.
- You can use the commands defined in the code or directly view them on Telegram by chatting with your own bot.

## Features:

- It supports language switching (Currently only between English and Spanish, you can add your own in the language file (/Modules/LangSupport/lang.yaml) with a few tweaks in the code).
- It sends metadata to the user about the song that will be downloaded.
- The metadata is accompanied by a thumbnail (from the video) in smaller dimensions to fit within the limits of Telebot/Telegram.
- Simple error handling (Virtually nonexistent).
- No advertisements (Avoiding potential copyright takedowns (the issue lies with users who misuse it)).

## Dependencies:
- FFMPEG

### Use pip install to install the following Python dependencies:
- pyTelegramBotAPI
- yt-dlp
- pillow
- pyYaml

## Tested:
- Currently only on Windows 10 x64.