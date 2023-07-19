import logging
import os
from datetime import date

from operations import trigger_reminders
from telegram_bot import bot
from fastapi import APIRouter
import telebot

logger = logging.getLogger("heb-dates")
DOMAIN = os.environ.get("DOMAIN")
router = APIRouter()


@router.get("/")
async def root():
    return {"status": "Healthy"}


@router.get("/echo/{chat_id}")
async def echo(chat_id: str):
    bot.send_message(chat_id, "echo")


@router.get("/trigger-today-reminders")
async def trigger_today_reminders():
    try:
        trigger_reminders()
    except Exception as e:
        logger.error("Failed to trigger reminders", exc_info=e)


@router.get("/trigger-reminders/{_date}")  # /trigger-reminders/24-5-2023
async def trigger_today_reminders(_date: str):
    try:
        date_parts = [int(elm) for elm in _date.split("-")]
        reminder_date = date(date_parts[2], date_parts[1], date_parts[0])
        trigger_reminders(reminder_date)
    except Exception:
        logger.exception("Failed to trigger reminders")


# Process webhook calls
@router.post(f'/telegram-hook')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@router.get("/remove-webhook")
def remove_webhook():
    bot.remove_webhook()


# Set webhook
@router.get("/set-webhook")
def set_webhook():
    bot.set_webhook(f"{DOMAIN}/telegram-hook")
