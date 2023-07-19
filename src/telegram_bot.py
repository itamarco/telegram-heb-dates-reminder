import os

import telebot

from user_flow import parse_input
from models.enums import OP

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@bot.message_handler(commands=["hello"])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hello Friend!")


def send_menu_keyboard(chat_id):
    # Create a custom keyboard with options
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add(OP.LIST_EVENTS.value, OP.DELETE_EVENT.value)

    # Send a welcome message with the custom keyboard
    bot.send_message(chat_id, "Welcome! Please choose an option:", reply_markup=keyboard)


def send_msg(chat_id, text):
    bot.send_message(chat_id, text)


@bot.message_handler(commands=["start"])
def handle_new_chat_member(message):
    chat_id = message.chat.id
    send_menu_keyboard(chat_id)


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_member(message):
    chat_id = message.chat.id
    send_menu_keyboard(chat_id)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = chat_id = message.chat.id
    ret_msg = parse_input(user_id, message.text)
    bot.send_message(chat_id, ret_msg)
