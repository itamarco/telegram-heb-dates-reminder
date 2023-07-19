import logging
from datetime import date

from app_flow import trigger_reminders
from main import app, DOMAIN
from telegram_bot import bot
import telebot

logger = logging.getLogger("heb-dates")


@app.get("/status")
async def root():
    return {"status": "Healthy"}


@app.get("/echo/{chat_id}")
async def echo(chat_id: str):
    bot.send_message(chat_id, "echo")


@app.get("/trigger-today-reminders")
async def trigger_today_reminders():
    try:
        trigger_reminders()
    except Exception as e:
        logger.error("Failed to trigger reminders", exc_info=e)


@app.get("/trigger-reminders/{_date}")  # /trigger-reminders/24-5-2023
async def trigger_today_reminders(_date: str):
    try:
        date_parts = [int(elm) for elm in _date.split("-")]
        reminder_date = date(date_parts[2], date_parts[1], date_parts[0])
        trigger_reminders(reminder_date)
    except Exception as e:
        logger.error("Failed to trigger reminders", exc_info=e)


# Process webhook calls
@app.post(f'/telegram-hook')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@app.get("/remove-webhook")
def remove_webhook():
    bot.remove_webhook()


# Set webhook
@app.get("/set-webhook")
def set_webhook():
    bot.set_webhook(f"{DOMAIN}/telegram-hook")
