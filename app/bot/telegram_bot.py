import logging

from bot.bot_impl import BotImpl, callback_action_delimiter
from user_flow import parse_freetext_input, handle_callback_actions

heb_date_bot = BotImpl()
