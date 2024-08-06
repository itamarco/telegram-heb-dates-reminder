import logging
import os
from datetime import date

import telebot

from custom_logger import logger
from app.db import reminder_dao
from operations import trigger_reminders
from bot.telegram_bot import heb_date_bot
from fastapi import APIRouter

from user_flow import parse_freetext_input

DOMAIN = os.environ.get("HOST")
router = APIRouter()


@router.get("/")
async def root():
    logger.info("root request")
    return {"status": "ok"}


@router.get("/db")
async def db_test():
    admin_id = os.environ.get("ADMIN_CHAT_ID")
    heb_date_bot.send_msg(admin_id, os.environ.get("SQLALCHEMY_POSTGRES_URL"))
    reminders = ["1"]
    try:
        reminders = reminder_dao.find_by_user(admin_id)
    except Exception as e:
        print(f"{e}")
    heb_date_bot.send_msg(admin_id, f"found reminders {len(reminders)}")


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
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").lower()

    bot_response = parse_freetext_input(chat_id, text)
    heb_date_bot.send_msg(chat_id, bot_response.text)


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


@router.get("/set-commands")
def set_commands():
    heb_date_bot.set_commands()
