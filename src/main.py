from fastapi import FastAPI
from telegram_bot import bot

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
