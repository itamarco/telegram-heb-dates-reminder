import re

from telebot.types import Message

from date_utils import heb_date_str_to_hebrew_date


def is_start_msg(message: Message):
    return message.text == 'start'


def is_date_msg(message: Message):
    try:
        heb_date_str_to_hebrew_date(message.text)
        return True
    except Exception as e:
        return False
