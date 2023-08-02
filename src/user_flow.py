import json
import logging
import re
from collections import defaultdict
from enum import Enum
from typing import Dict

from pyluach.dates import HebrewDate

from date_utils import heb_date_str_to_hebrew_date
from db import reminder_dao
from models.bot_response import BotResponse
from models.context import Context
from models.enums import TEXTS, OP, TEXT_FORMATS, CALLBACK_ACTION
from operations import add_reminder, pretty_print_reminder, get_event_titles
from text_patterns import is_date_msg, date_string_has_year

logger = logging.getLogger("heb-dates")


class LastStage(str, Enum):
    DATE_PROVIDED = "DATE_PROVIDED",
    EVENT_DESCRIPTION = "EVENT_DESCRIPTION",
    REMINDER_DAYS = "REMINDER_DAYS",


_context: Dict[int, Context] = {}


def parse_freetext_input(user_id: int, text: str) -> BotResponse:
    context = _context.get(user_id)
    if is_date_msg(text):
        heb_date = heb_date_str_to_hebrew_date(text)

        context = Context(user_id)
        context.last_stage = LastStage.DATE_PROVIDED
        context.heb_date_tuple = (
            heb_date.year if date_string_has_year(text) else None,  # TODO refactor
            heb_date.month,
            heb_date.day
        )

        _context[user_id] = context
        return BotResponse(TEXTS.SET_DESCRIPTION.value)

    elif context and context.last_stage == LastStage.DATE_PROVIDED:
        context.last_stage = LastStage.EVENT_DESCRIPTION
        context.description = text
        return BotResponse(TEXTS.SET_REMINDER_DAYS.value)

    elif context and context.last_stage == LastStage.EVENT_DESCRIPTION:
        context.last_stage = LastStage.REMINDER_DAYS
        reminder_days_list = [int(days) for days in re.split(r'\s+|,', text)]
        for reminder_days in reminder_days_list:
            add_reminder(
                user_id=user_id,
                date_tuple=context.heb_date_tuple,
                description=context.description,
                reminder_days=reminder_days)

        del _context[user_id]
        return BotResponse(f"{TEXTS.REMINDER_ADDED.value}")

    elif text == OP.LIST_REMINDERS.value:
        reminders = reminder_dao.find_by_user(user_id)
        response_lines = [
            pretty_print_reminder(reminder) for reminder in reminders
        ]
        return BotResponse("\n".join(response_lines) + "\n")

    elif text == OP.LIST_EVENTS.value:
        reminders = reminder_dao.find_by_user(user_id)
        event_reminders = defaultdict(list)
        event_dates = {}
        for reminder in reminders:
            year = reminder.eventYear or HebrewDate.today().year
            heb_date = HebrewDate(year, reminder.eventMonth, reminder.eventDay)
            event_reminders[reminder.description].append(str(reminder.reminderDays))
            event_dates[reminder.description] = heb_date.hebrew_date_string()

        return BotResponse("\n".join([
            TEXT_FORMATS.EVENT_PRETTY_PRINT.format(
                title=title,
                date=event_dates[title],
                reminder_days_list=", ".join(event_reminders[title])
            )
            for title in event_dates.keys()
        ]))

    elif text == OP.DELETE_EVENT.value:
        event_titles = get_event_titles(user_id)
        response = BotResponse(TEXTS.CLICK_EVENT_TO_DELETE)
        response.add_inline_items(
            action="delete",
            items_display=event_titles,
            items_callback_data=event_titles
        )

        return response

    elif text == OP.INSTRUCTIONS.value:
        return BotResponse(TEXTS.INSTRUCTIONS)

    else:
        return BotResponse(TEXTS.FLOW_ERROR.value)


def handle_callback_actions(user_id, action, data):
    if action == CALLBACK_ACTION.DELETE.value:
        reminder_dao.delete_by_userid_description(user_id, data)
        return BotResponse(TEXT_FORMATS.EVENT_DELETED.format(title=data))
