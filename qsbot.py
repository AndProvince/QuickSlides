# PDF slides generator
# by Andrey Ponomarev
# 4ponomarev@gmail.com

import os
import telebot

from quckslides import create_slides
from dotenv import load_dotenv

load_dotenv('settings.env')

BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot.reply_to(message, 'Hello!\n'
                          'Welcome to QuickSlides\n'
                          'I can convert your message into PDF slides\n'
                          'Send me multiline message: one line = one slide\n'
                          'Format each line as follows: Topic name / Topic body')


@bot.message_handler(content_types=['photo', 'document'])
def bot_message(message):
    bot.reply_to(message, 'Please send text message')


@bot.message_handler(content_types=['text'])
def photo(message):
    bot.reply_to(message, 'Ok, let\'s try.\n'
                          'Please wait a moment while the slides are being created.')
    input_texts = []
    for line in message.text.split('\n'):
        input_texts.append(line.split('/', 1))

    create_slides(input_texts)

    file = open('output/QuickSlides.pdf', 'rb')
    bot.send_document(message.chat.id, file)


if __name__ == '__main__':
    bot.infinity_polling()
