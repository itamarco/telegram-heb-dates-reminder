import os
from typing import Tuple, List

import telebot

from user_flow import parse_input
from models.enums import OP, TEXT_FORMATS, TEXTS

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
callback_action_delimiter = "::"


def send_menu_keyboard(chat_id):
    # Create a custom keyboard with options
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
    keyboard.add(OP.INSTRUCTIONS, OP.LIST_REMINDERS)
    keyboard.add(OP.LIST_EVENTS.value, OP.DELETE_EVENT.value)

    # Send a welcome message with the custom keyboard
    bot.send_message(chat_id, TEXTS.WELCOME, reply_markup=keyboard)


def send_msg(chat_id, text):
    bot.send_message(chat_id, text)


def send_inline_buttons(chat_id, title, items: List[Tuple[str, str]], action: str = None):
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for item in items:
        callback_text = f"{action}{callback_action_delimiter}{item[1]}" if action else item[1]
        button = telebot.types.InlineKeyboardButton(text=item[0], callback_data=callback_text)
        inline_markup.add(button)

    bot.send_message(chat_id, title, reply_markup=inline_markup)


@bot.message_handler(commands=["start"])
def handle_new_chat_member(message):
    chat_id = message.chat.id
    send_menu_keyboard(chat_id)


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_member(message):
    chat_id = message.chat.id
    send_menu_keyboard(chat_id)


@bot.message_handler(func=lambda message: message.text == "התחל")
def parse_with_context(message):
    chat_id = message.chat.id
    send_menu_keyboard(chat_id)
    

@bot.message_handler(func=lambda message: message.text == OP.DELETE_EVENT.value)
def delete_event_op(message):
    chat_id = message.chat.id
    send_inline_buttons(chat_id, )


@bot.message_handler(func=lambda message: True)
def parse_with_context(message):
    user_id = chat_id = message.chat.id
    ret_msg = parse_input(user_id, message.text)
    send_msg(chat_id, ret_msg)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = chat_id = call.message.chat.id
    # 'call.data' contains the value that was sent back to the bot when the item was clicked
    ret_msg = parse_input(user_id, call.data)
    send_msg(chat_id, ret_msg)
