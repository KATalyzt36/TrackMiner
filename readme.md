# Track Miner

![Track Miner Logo](https://avatars.githubusercontent.com/u/129672059?v=4 "Track Miner Logo")

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

### Install all dependencies:
`pip install -r requirements.txt`

## Tested:
- Windows 10 x64.
- Linux x64.
- Github CodeSpaces.
