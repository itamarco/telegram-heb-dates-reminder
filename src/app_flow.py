import json
from enum import Enum
from typing import Dict, Any

from datetime import date
from pyluach.dates import HebrewDate

from date_utils import heb_date_str_to_hebrew_date
from db import reminderDao
from models.context import Context, DateTuple
from models.reminder import Reminder
from text_patterns import is_date_msg, date_string_has_year


class LastStage(str, Enum):
    DATE_PROVIDED = "DATE_PROVIDED",
    EVENT_DESCRIPTION = "EVENT_DESCRIPTION",
    REMINDER_DAYS = "REMINDER_DAYS",


class OP(str, Enum):
    LIST_EVENTS = "רשימת תזכורות",
    DELETE_EVENT = "מחק תזכורת",


class TEXTS(str, Enum):
    SET_DESCRIPTION = "תיאור קצר של האירוע:",
    SET_REMINDER_DAYS = "כמה ימים מראש להתריע?",
    REMINDER_ADDED = "תזכורת התווספה בהצלחה",
    FLOW_ERROR = "Internal flow error"


_context: Dict[int, Context] = {}


def add_reminder(user_id, date_tuple: DateTuple, description, reminder_days):
    (heb_year, heb_month, heb_day) = date_tuple
    next_reminder = calc_next_reminder_date(date_tuple, reminder_days)
    reminder = Reminder(
        userId=user_id,
        description=description,
        eventDay=heb_day,
        eventMonth=heb_month,
        eventYear=heb_year,
        reminderDays=reminder_days,
        nextReminder=next_reminder,
        repeat=True  # TODO heb_date <= today
    )
    reminderDao.create(reminder)
    return reminder.id


def calc_next_reminder_date(date_tuple: DateTuple, reminder_days: int):
    (heb_year, heb_month, heb_day) = date_tuple

    current_year_date = HebrewDate(HebrewDate.today().year, heb_month, heb_day)

    heb_date = HebrewDate(heb_year, heb_month, heb_day) if heb_year else current_year_date

    today = HebrewDate.today()

    next_reminder: date = date.today()
    # TODO refactor
    if heb_date > today and heb_date - reminder_days > today:
        next_reminder = (heb_date - reminder_days).to_pydate()
    elif heb_date < today < (current_year_date - reminder_days):
        next_reminder = (current_year_date - reminder_days).to_pydate()
    elif heb_date < today and (current_year_date - reminder_days) < today:
        next_reminder = (current_year_date.add(years=1) - reminder_days).to_pydate()

    return next_reminder


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
        reminders = [reminder.to_dict() for reminder in reminderDao.find_by_user(user_id)]
        return json.dumps(reminders, ensure_ascii=False).encode('utf8')

    else:
        return TEXTS.FLOW_ERROR.value
