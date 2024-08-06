import os
from typing import List

import telebot

from models.enums import OP, TEXT_FORMATS, TEXTS
from user_flow import parse_freetext_input

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

callback_action_delimiter = "::"


class BotImpl:
    def __init__(self):
        self.bot = None

    def get_bot(self):
        return self.bot

    def polling(self):
        self.bot.infinity_polling()

    def set_webhook(self, url):
        self.bot.set_webhook(url)

    def unset_webhook(self):
        self.bot.remove_webhook()

    def send_menu_keyboard(self, chat_id):
        # Create a custom keyboard with options
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
        keyboard.add(OP.INSTRUCTIONS, OP.LIST_REMINDERS)
        keyboard.add(OP.LIST_EVENTS.value, OP.DELETE_EVENT.value)

        # Send a welcome message with the custom keyboard
        self.bot.send_message(chat_id, TEXTS.WELCOME, reply_markup=keyboard)

    def send_msg(self, chat_id, text):
        url = f"{TELEGRAM_API_BASE_URL}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text
        }
        requests.get(url, params=params)

    def send_inline_buttons(self, chat_id, title, items_display: List[str], items_callback_data: List[str],
                            action: str = None):
        if len(items_display) != len(items_callback_data):
            raise ValueError("items_display and items_callback_data are not at the same length")

        inline_markup = telebot.types.InlineKeyboardMarkup()
        for display, callback in zip(items_display, items_callback_data):
            callback_text = f"{action}{callback_action_delimiter}{callback}" if action else callback
            button = telebot.types.InlineKeyboardButton(text=display, callback_data=callback_text)
            inline_markup.add(button)

        self.bot.send_message(chat_id, title, reply_markup=inline_markup)
