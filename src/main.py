from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.reminder import Base, ReminderDAO
from telegram_bot import bot

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


print("Starting bot")
bot.infinity_polling()

# import asyncio
# import uvicorn
#
# asyncio.run(bot.polling())
#
# uvicorn.run(app)
