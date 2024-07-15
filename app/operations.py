import logging
from collections import defaultdict
from datetime import date
from typing import Dict

from app.db import reminder_dao
from app.models.context import DateTuple
from app.models.enums import TEXT_FORMATS
from app.models.reminder import Reminder
from pyluach.dates import HebrewDate

logger = logging.getLogger("heb-dates")

"""
    :argument reminder_date
"""


def trigger_reminders(reminder_date: date = date.today()) -> int:
    """
        Trigger reminders for a specified date.

        This function fetches reminders from the database for the given date and sends notifications to the users
        with reminders on this date. After sending notifications, it updates the reminders in the database
        to set the 'lastReminder' and 'nextReminder' fields accordingly.

        Parameters:
            reminder_date (date, optional): The date for which reminders need to be triggered.
                Defaults to today's date if not specified.

        Returns:
            int: The number of reminders triggered successfully.
    """
    logger.info(f"Triggering reminders for {reminder_date}")
    today_reminders = reminder_dao.find_by_date(reminder_date)
    logger.info(f"Found {len(today_reminders)} reminders")
    notifications = defaultdict(list)
    for reminder in today_reminders:
        reminder.last_reminder = reminder.next_reminder
        reminder.next_reminder = None if not reminder.repeat else calc_next_reminder_date(
            (HebrewDate.today().year + 1, reminder.event_month, reminder.event_day), reminder.reminder_days)

        notifications[reminder.user_id].append(reminder)

    logger.info("Send notifications for users")
    send_notifications(notifications)
    logger.info("Updating reminders in DB")
    reminder_dao.update_all(today_reminders)
    logger.info("Reminders triggered successfully!")
    return len(notifications)


def send_notifications(notifications_dict: Dict[str, Reminder]):
    from bot.telegram_bot import heb_date_bot  # refactor
    for chat_id in notifications_dict.keys():
        for reminder in notifications_dict.get(chat_id):
            heb_date_bot.send_msg(chat_id,
                                  TEXT_FORMATS.EVENT_IS_COMING.format(days=reminder.reminder_days,
                                                                      event=reminder.description))


def add_reminder(user_id, date_tuple: DateTuple, description, reminder_days):
    (heb_year, heb_month, heb_day) = date_tuple
    next_reminder = calc_next_reminder_date(date_tuple, reminder_days)
    reminder = Reminder(
        user_id=user_id,
        description=description,
        event_day=heb_day,
        event_month=heb_month,
        event_year=heb_year,
        reminder_days=reminder_days,
        next_reminder=next_reminder,
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


def pretty_print_reminder(reminder: Reminder) -> str:
    year = reminder.event_year or HebrewDate.today().year
    heb_date = HebrewDate(year, reminder.event_month, reminder.event_day)

    return TEXT_FORMATS.REMINDER_PRETTY_PRINT.format(
        id=reminder.id,
        title=reminder.description,
        date=heb_date.hebrew_date_string(),
        reminder_days=reminder.reminder_days,
        next_reminder=reminder.next_reminder
    )


def get_event_titles(user_id):
    reminders = reminder_dao.find_by_user(user_id)
    events = set([reminder.description for reminder in reminders])
    return events
