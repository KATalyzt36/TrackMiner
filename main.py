### General imports
from config import *
from consts import *
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import yaml
import re

### MODULES
from Modules import regex, image_handler, format, ytdlp, download, color, paths
from Modules.LangSupport.lang_support import Database

# Options
useCustomFFMPEG = True # If this is true, uses your ffmpeg from './ffmpeg/bin' else use your system ffmpeg
ffmpegRoute = paths.convert_to_windows("ffmpeg/bin") # Fill this if "useCustomFFMPEG" is "True"
ffmpegExec = ffmpegRoute + paths.convert_to_windows("/ffmpeg.exe")

### CODE
TOKEN = ""
ENV_TOKEN = os.environ.get("TRACK_MINER_TOKEN")
if ENV_TOKEN != None:
    TOKEN = ENV_TOKEN
else:
    TOKEN = TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TOKEN)
#bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
db_path = 'Modules/LangSupport/lang_for_user.db'

# Charge Langs
with open('Modules/LangSupport/lang.yaml', 'r', encoding='utf-8') as f:
    lang = yaml.safe_load(f)


# Functions
def get_msg(lang_code, msg_key, **kwargs):
    return lang[lang_code][msg_key].format(**kwargs)  # get_msg('es','help', variable=valor_variable)


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🇺🇸 English", callback_data="cb_english"),
               InlineKeyboardButton("🇪🇸 Español", callback_data="cb_spanish"))
    return markup


def print_error(e, col='red', notas=""):
    if col == 'red':
        print("\033[91m")
    print(notas)
    print(e)
    print("\033[0m")


def set_lang(call, lang):
    db = Database(db_path)
    chat_id = call.json["message"]["chat"]["id"]
    msg_id = call.message.id

    db.set_language(call.from_user.id, lang)
    bot.edit_message_text(chat_id=chat_id, message_id=msg_id,
                          text=get_msg(db.get_language(call.from_user.id), 'lang_changed'))
    bot.answer_callback_query(call.id, get_msg(db.get_language(call.from_user.id), 'lang_changed'))


# Framework Telebot Comms
@bot.message_handler(commands=['start'])
def cmd_start(message):
    db = Database(db_path)
    db.create_table()
    bot.reply_to(message,
                 get_msg(db.get_language(message.from_user.id), 'hi', user=message.from_user.first_name),
                 parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def cmd_start(message):
    db = Database(db_path)
    bot.reply_to(message,
                 get_msg(db.get_language(message.from_user.id), 'help'),
                 disable_web_page_preview=True)


@bot.message_handler(commands=['contact'])
def cmd_start(message):
    db = Database(db_path)
    bot.reply_to(message,
                 get_msg(db.get_language(message.from_user.id), 'contact'))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_english":
        set_lang(call, 'en')
    elif call.data == "cb_spanish":
        set_lang(call, 'es')


@bot.message_handler(commands=['lang'])
def cmd_start(message):
    db = Database(db_path)
    bot.send_message(message.chat.id, text=get_msg(db.get_language(message.from_user.id), 'lang'), reply_markup=gen_markup())


@bot.message_handler(commands=['clear_db'])
def cmd_start(message):
    if message.from_user.id == 351760926: # Your ID
        db = Database(db_path)
        db.clear_db()
        bot.send_message(message.chat.id, "Db cleared")


@bot.message_handler(commands=['active'])
def cmd_start(message):
    db = Database(db_path)
    bot.send_message(message.chat.id, "✅"+ get_msg(db.get_language(message.from_user.id), "active") +"✅")

@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    db = Database(db_path)

    if message.text.startswith("/"):
        bot.reply_to(message, get_msg(db.get_language(message.from_user.id), 'command_doesnt_exist'))
    else:
        if any(message.text.startswith(prefix) for prefix in URLS):
            url = message.text
            if url.find("&list") != -1:
                bot.reply_to(message,
                             get_msg(db.get_language(message.from_user.id), 'error_playlist_in_url'),
                             disable_web_page_preview=True)
                url = re.sub(r"&list=.*", "", url)

            waiting_msg = bot.reply_to(message, get_msg(db.get_language(message.from_user.id), 'obtaining_info'), parse_mode="Markdown")

            try:
                title, channel, duration, filesize, artist, thumbnail, n_title = ytdlp.download_song(url)
                duration = format.duration(duration)
                filesize = format.size(filesize)
                n_title = regex.get_nombre(n_title)
                if artist is None:
                    artist = channel

                bot.delete_message(message.chat.id, waiting_msg.message_id)

                download.file(thumbnail, n_title)

                if not thumbnail.endswith(".jpg"):
                    image_handler.convert_to_jpg(n_title)
                image_handler.thumbnail_compatible(n_title)

                with open(f'Downloads/{n_title}.jpg', 'rb') as f:
                    image = f.read()

                information = bot.send_photo(message.chat.id, image, caption=get_msg(db.get_language(message.from_user.id), 'file_info',
                                                                                    title=title,
                                                                                    channel=channel,
                                                                                    duration=duration,
                                                                                    filesize=filesize) + "\n" +
                                                                                    get_msg(db.get_language(message.from_user.id), 'preparing_file'),
                                                                                        parse_mode="Markdown")

                bot.send_chat_action(message.chat.id, 'upload_audio')

                if useCustomFFMPEG:
                    os.system(ffmpegExec + f' -i Downloads/{n_title}.m4a -c:v copy -c:a libmp3lame -q:a 4 Downloads/{n_title}.mp3')
                else:
                    os.system(f'ffmpeg -i Downloads/{n_title}.m4a -c:v copy -c:a libmp3lame -q:a 4 Downloads/{n_title}.mp3')

                with open(f"Downloads/{n_title}.mp3", 'rb') as audio:
                    with open(f"Downloads/{n_title}.jpg", 'rb') as thumbnail:
                        if channel in title:
                            bot.send_audio(message.chat.id, audio, title=title, thumbnail=thumbnail)
                        else:
                            bot.send_audio(message.chat.id, audio, title=title, thumbnail=thumbnail, performer=artist)

                bot.edit_message_caption(chat_id=message.chat.id, message_id=information.message_id, caption=get_msg(db.get_language(message.from_user.id), 'file_info',
                                                                                    title=title,
                                                                                    channel=channel,
                                                                                    duration=duration,
                                                                                    filesize=filesize) + "\n" +
                                                                                    get_msg(db.get_language(message.from_user.id), 'file_sent'),
                                                                                        parse_mode="Markdown")

                os.remove(f'Downloads/{n_title}.jpg')
                os.remove(f'Downloads/{n_title}.m4a')
                os.remove(f'Downloads/{n_title}.mp3')

            except Exception as e:
                bot.reply_to(message, get_msg(db.get_language(message.from_user.id), 'error_to_download_info'))
                print_error(e, 'red')
            return

        bot.reply_to(message, get_msg(db.get_language(message.from_user.id), 'no_link_received'))


if __name__ == '__main__':
    os.system('clear')
    print(f"{color.GREEN}@@@ TRACK MINER BOT STARTED @@@{color.RESET}")
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "👋 Launch bot"),
        telebot.types.BotCommand("/help", "✏ A little help"),
        telebot.types.BotCommand("/contact", "🐛 Have you found any bugs or do you have any questions?"),
        telebot.types.BotCommand("/lang", "🌎 Change language")
    ])
    bot.infinity_polling()
