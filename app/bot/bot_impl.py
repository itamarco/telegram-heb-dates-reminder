import os
from typing import List

import requests


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

callback_action_delimiter = "::"


class BotImpl:
    def send_msg(self, chat_id, text):
        url = f"{TELEGRAM_API_BASE_URL}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text
        }
        requests.get(url, params=params)

