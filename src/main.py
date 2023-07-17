import os

import telebot
import uvicorn
from fastapi import FastAPI

from telegram_bot import bot, TELEGRAM_TOKEN

DOMAIN = os.environ.get("DOMAIN")
app = FastAPI()


@app.get("/status")
def root():
    return {"status": "Healthy"}


# Process webhook calls
@app.post(f'telegram-hook/{TELEGRAM_TOKEN}/')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


bot.remove_webhook()

# Set webhook
bot.set_webhook(f"{DOMAIN}/telegram-hook")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
