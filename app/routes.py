import logging
import os
from datetime import date

import telebot

from operations import trigger_reminders
from bot.telegram_bot import heb_date_bot
from fastapi import APIRouter

logger = logging.getLogger("heb-dates")
DOMAIN = os.environ.get("HOST")
router = APIRouter()


@router.get("/")
async def root():
    return {"status": "ok"}


@router.get("/db")
async def db_test():
    import os
    import psycopg2

    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DATABASE'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    print("Database connection established.")
    cur = conn.cursor()
    # Define the query
    query = "SELECT * FROM reminder;"

    # Execute the query
    try:
        cur.execute(query)
        # Fetch all results
        reminders = cur.fetchall()

        # Process the results
        print(f"{len(reminders)} entries")
        for reminder in reminders:
            print(reminder)
    except Exception as e:
        print(f"Error executing query: {e}")


@router.get("/echo/{chat_id}")
async def echo(chat_id: str):
    heb_date_bot.send_msg(chat_id, "echo")


@router.get("/trigger-today-reminders")
async def trigger_today_reminders():
    today = date.today()
    return await trigger_reminders_by_date(f"{today.day}-{today.month}-{today.year}")


@router.get("/trigger-reminders/{_date}")  # /trigger-reminders/24-5-2023
async def trigger_reminders_by_date(_date: str):
    try:
        date_parts = [int(elm) for elm in _date.split("-")]
        reminder_date = date(date_parts[2], date_parts[1], date_parts[0])
        total_triggered_reminders = trigger_reminders(reminder_date)
        return {"status": f"Total reminders: {total_triggered_reminders}"}
    except Exception as e:
        logger.exception("Failed to trigger reminders")
        return {"status": f"Failure {e}"}


@router.post(f'/telegram-hook')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        heb_date_bot.get_bot().process_new_updates([update])
    else:
        return


@router.get("/remove-webhook")
def remove_webhook():
    logger.warning("Telegram webhook unset!")
    heb_date_bot.unset_webhook()


# Set webhook
@router.get("/set-webhook")
def set_webhook():
    webhook = f"{DOMAIN}/telegram-hook"
    logger.info("setting telegram webhook: %s", webhook)
    heb_date_bot.set_webhook(webhook)
