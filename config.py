import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMINCHAT = os.getenv('CHAT')
ADMIN_1 = os.getenv('ADMIN_1')
ADMIN_2 = os.getenv('ADMIN_2')

if TELEGRAM_TOKEN is None:
    raise Exception("Переменная <TELEGRAM_TOKEN> не установлена.")

if ADMINCHAT is None:
    raise Exception("Переменная <CHAT> не установлена.")


forwarded_content = {'text', 'sticker', 'photo', 'document', 'audio', 'media',
                     'animation', 'video', 'voice', 'video_note', 'vcard'}

SAY_HELLO = 'Здравствуйте, '
SAY_HELP = 'Напишите ваш вопрос и мы ответим Вам в ближайшее время'
START_BOT = '<i>SFBbot запущен</i>\n<b>Белогор заступает на дежурство!</b>'
STOP_BOT = '<i>SFBbot остановлен!</i>\n<b>Белогор пошел спать!</b>'
