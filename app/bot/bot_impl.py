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

    def set_commands(self):
        url = f"{TELEGRAM_API_BASE_URL}/setMyCommands"
        payload = {
            "commands": [
                {"command": "start", "description": "Get instructions"},
                {"command": "events", "description": "Events list"},
                {"command": "reminders", "description": "Reminders list"},
                {"command": "delete", "description": "Delete event"},
                {"command": "today", "description": "Today's date"}
            ]
        }

        requests.post(url, json=payload)
