import logging
from collections import defaultdict
from datetime import date
from typing import Dict

from db import reminder_dao
from models.context import DateTuple
from models.reminder import Reminder
from telegram_bot import send_msg
from pyluach.dates import HebrewDate

logger = logging.getLogger("heb-dates")


def trigger_reminders(reminder_date: date = date.today()):
    logger.info(f"Triggering reminders for {reminder_date}")
    today_reminders = reminder_dao.find_by_date(reminder_date)
    logger.info(f"Found {len(today_reminders)} reminders")
    notifications = defaultdict(list)
    for reminder in today_reminders:
        reminder.lastReminder = reminder.nextReminder
        reminder.nextReminder = calc_next_reminder_date(
            (reminder.eventYear, reminder.eventMonth, reminder.eventDay), reminder.reminderDays)

        notifications[reminder.userId].append(reminder)

    logger.info("Send notifications for users")
    send_notifications(notifications)
    logger.info("Updating reminders in DB")
    reminder_dao.update_all(today_reminders)
    logger.info("Reminders triggered successfully!")


def send_notifications(notifications_dict: Dict[str, Reminder]):
    for chat_id in notifications_dict.keys():
        for reminder in notifications_dict.get(chat_id):
            send_msg(chat_id, f"בעוד {reminder.reminderDays} ימים: {reminder.description}")


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
