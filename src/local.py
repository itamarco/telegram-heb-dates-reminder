import logging
from threading import Thread
import uvicorn
from telegram_bot import bot


def blocking():
    print("Starting bot")
    bot.infinity_polling()


if __name__ == "__main__":
    thread = Thread(target=blocking)
    thread.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=logging.INFO)
