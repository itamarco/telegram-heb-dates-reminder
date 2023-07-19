import json
import logging
from enum import Enum
from typing import Dict

from date_utils import heb_date_str_to_hebrew_date
from db import reminder_dao
from models.context import Context
from models.enums import TEXTS, OP
from text_patterns import is_date_msg, date_string_has_year

logger = logging.getLogger("heb-dates")


class LastStage(str, Enum):
    DATE_PROVIDED = "DATE_PROVIDED",
    EVENT_DESCRIPTION = "EVENT_DESCRIPTION",
    REMINDER_DAYS = "REMINDER_DAYS",


_context: Dict[int, Context] = {}


def parse_input(user_id: int, text: str) -> str:
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
        return TEXTS.SET_DESCRIPTION.value

    elif context and context.last_stage == LastStage.DATE_PROVIDED:
        context.last_stage = LastStage.EVENT_DESCRIPTION
        context.description = text
        return TEXTS.SET_REMINDER_DAYS.value

    elif context and context.last_stage == LastStage.EVENT_DESCRIPTION:
        context.last_stage = LastStage.REMINDER_DAYS
        reminder_days = int(text)
        reminder_id = add_reminder(
            user_id=user_id,
            date_tuple=context.heb_date_tuple,
            description=context.description,
            reminder_days=reminder_days)

        del _context[user_id]
        return f"{TEXTS.REMINDER_ADDED.value} {reminder_id}"

    elif text == OP.LIST_EVENTS.value:
        reminders = [reminder.to_dict() for reminder in reminder_dao.find_by_user(user_id)]
        return json.dumps(reminders, ensure_ascii=False).encode('utf8')

    else:
        return TEXTS.FLOW_ERROR.value
