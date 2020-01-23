#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import telegram
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from api import search_serial

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

TOKEN = '985605064:AAEycN70aUGV7H2lSW_UsqxQmb5Yl0MOuzI'
SOCKS_URL = 'socks5://s5.priv.opennetwork.cc:1080'
SOCKS_USER = 'v3_420155450'
SOCKS_PASS = 'DvX2NoIP'


def get_random_smile():
    # function of random selection of meaning from the list
    smiles = [
        '🙃',
        '☺️',
        '😃',
        '😉',
        '😇',
        '😊',
        '😚',
        '😋',
        '😜',
        '🤩'
    ]
    return random.choice(smiles)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message and keyboard when the command /start is issued."""
    # update.message.reply_text('Hi!')
    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    buttons = [['🔎 Search', '📕 Subscriptions']]
    keyboard = telegram.ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    context.bot.send_message(user_id, 'Hi, 'f'{name}!', reply_markup=keyboard)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('You have come to the right place!\n'
                              '⭕️In order to find the show you need to write me a message\n' 
                              '⭕️In order to subscribe/unsubscribe to the newsletter of the series,'
                              ' you must find the desired series and click on the subscribe/unsubscribe '
                              'button and receive the appropriate notification\n'
                              '⭕️For other questions write to my developer @Green_Brosha')


def telegram_id(update, context):
    # function that returns user id
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    context.bot.send_message(user_id, f'Hello {get_random_smile()}')
    update.message.reply_text(f'{name}, Your id: {user_id}')


def inline_keyboard_handler(update, context):
    # buttons that are created in the message box
    message_text = update.message.text

    serial_info = search_serial(message_text)

    keyboard = []

    for serial in serial_info:
        keyboard.append([InlineKeyboardButton(f'{serial["show"]["name"]}', callback_data=serial["show"]["id"])])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    # responsible for pressing buttons
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))


def echo(update, context):
    # exception handling for incoming messages from users
    if 'Search' in update.message.text:
        update.message.reply_text(
            f'Write me in the 🔽message🔽 the name of the series that you find {get_random_smile()}')
    else:
        inline_keyboard_handler(update, context)


def action_processing(update, context):
    # handling button presses
    keyboard = [InlineKeyboardButton("Subscribe", callback_data='Ok!')]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Would you like to subscribe?', reply_markup=reply_markup)

    keyboard = [InlineKeyboardButton("Unsubscribe", callback_data='Ok!')]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Would you like to unsubscribe?', reply_markup=reply_markup)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # updater = Updater("TOKEN", use_context=True)

    updater = Updater(
        TOKEN, use_context=True,
        request_kwargs={
            'proxy_url': SOCKS_URL,
            'urllib3_proxy_kwargs': {'username': SOCKS_USER, 'password': SOCKS_PASS},
        },
    )
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("telegram_id", telegram_id))

    # responsible for drawing buttons in the keyboard
    dp.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
