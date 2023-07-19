import json
import logging
from collections import defaultdict
from enum import Enum
from typing import Dict

from datetime import date
from pyluach.dates import HebrewDate

from date_utils import heb_date_str_to_hebrew_date
from db import reminder_dao
from models.context import Context, DateTuple
from models.reminder import Reminder
from models.enums import TEXTS, OP
from telegram_bot import send_msg
from text_patterns import is_date_msg, date_string_has_year

logger = logging.getLogger("heb-dates")


class LastStage(str, Enum):
    DATE_PROVIDED = "DATE_PROVIDED",
    EVENT_DESCRIPTION = "EVENT_DESCRIPTION",
    REMINDER_DAYS = "REMINDER_DAYS",


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
    reminder_dao.create(reminder)
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
        reminders = [reminder.to_dict() for reminder in reminder_dao.find_by_user(user_id)]
        return json.dumps(reminders, ensure_ascii=False).encode('utf8')

    else:
        return TEXTS.FLOW_ERROR.value


def trigger_reminders(reminder_date: date = date.today()):
    logger.info(f"Triggering reminders for {reminder_date}")
    today_reminders = reminder_dao.find_by_date(reminder_date)
    logger.info(f"Found {len(today_reminders)} reminders")
    notifications = defaultdict(list)
    for reminder in today_reminders:
        reminder.lastReminder = reminder.nextReminder
        reminder.nextReminder = calc_next_reminder_date(
            (reminder.eventYear, reminder.eventMonth, reminder.eventDay), reminder.reminderDays)

        notifications.get(reminder.userId).append(reminder)

    logger.info("Send notifications for users")
    send_notifications(notifications)
    logger.info("Updating reminders in DB")
    reminder_dao.update_all(today_reminders)
    logger.info("Reminders triggered successfully!")


def send_notifications(notifications_dict: Dict[str, Reminder]):
    for chat_id in notifications_dict.keys():
        for reminder in notifications_dict.get(chat_id):
            send_msg(chat_id, f"בעוד {reminder.reminderDays} ימים: {reminder.description}")
