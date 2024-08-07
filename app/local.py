import logging
from dotenv import load_dotenv

load_dotenv("../.env.local")
from threading import Thread
import uvicorn
from bot.telegram_bot import heb_date_bot


def start_bot():
    print("Starting bot")
    heb_date_bot.polling()


if __name__ == "__main__":
    thread = Thread(target=start_bot)
    thread.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=logging.INFO)
