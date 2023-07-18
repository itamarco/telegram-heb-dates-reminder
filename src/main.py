import os

import telebot
import uvicorn
from fastapi import FastAPI

from telegram_bot import bot

DOMAIN = os.environ.get("DOMAIN")
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
