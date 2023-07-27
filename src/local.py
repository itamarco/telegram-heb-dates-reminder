import logging
import uvicorn

from telegram_bot import bot

print("Starting bot")

bot.infinity_polling()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level=logging.INFO)
