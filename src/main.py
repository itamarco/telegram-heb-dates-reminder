from fastapi import FastAPI
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
