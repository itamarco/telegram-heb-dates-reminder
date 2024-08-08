import json
import os

import requests

from models.bot_response import BotResponse
from user_flow import parse_freetext_input, handle_callback_actions

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

callback_action_delimiter = "::"


class BotImpl:
    def send_msg(self, chat_id, response: BotResponse):
        url = f"{TELEGRAM_API_BASE_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": response.text,
            "parse_mode": "Markdown"
        }
        if response.inline_buttons:
            payload['reply_markup'] = self.to_online_keyboard(response.inline_buttons)
        requests.post(url, json=payload)

    def to_online_keyboard(self, inline_buttons: list[tuple[str, str]]) -> json:
        keyboard = [[dict(text=btn_text, callback_data=btn_data)] for btn_text, btn_data in inline_buttons]

        return json.dumps({"inline_keyboard": keyboard})

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

    def unset_webhook(self):
        url = f"{TELEGRAM_API_BASE_URL}/deleteWebhook"
        requests.get(url)

    def set_webhook(self, webhook):
        url = f"{TELEGRAM_API_BASE_URL}/setWebhook"
        payload = {"url": webhook}
        requests.post(url, json=payload)

    def polling(self):
        offset = 0
        while True:
            url = f"{TELEGRAM_API_BASE_URL}/getUpdates?offset={offset}"
            response = requests.get(url)
            result = response.json()

            if result['ok']:
                for update in result['result']:
                    offset = update['update_id'] + 1
                    self.process_update(update)

    def process_update(self, update):
        if "message" in update:
            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "").lower()
            bot_response = parse_freetext_input(chat_id, text)
            self.send_msg(chat_id, bot_response)

        elif 'callback_query' in update:
            callback_query = update.get("callback_query")
            message_id = callback_query.get("message", {}).get("message_id")
            chat_id = callback_query.get("from", {}).get("id")
            data = callback_query.get("data")

            [op, info] = data.split(callback_action_delimiter)
            bot_response = handle_callback_actions(chat_id, op, info)
            self.edit_msg(chat_id, message_id, bot_response)

    def edit_msg(self, chat_id, message_id, bot_response: BotResponse):
        url = f"{TELEGRAM_API_BASE_URL}/editMessageText"
        payload = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': bot_response.text
        }
        requests.post(url, json=payload)
