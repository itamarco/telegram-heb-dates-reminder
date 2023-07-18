from main import app


@app.get("/status")
def root():
    return {"status": "Healthy"}


# Process webhook calls
@app.post(f'/telegram-hook')
def process_webhook(update: dict):
    if update:
        update = telebot.types.Update.de_json(update)
        bot.process_new_updates([update])
    else:
        return


@app.get("/remove-webhook")
def remove_webhook():
    bot.remove_webhook()


# Set webhook
@app.get("/set-webhook")
def set_webhook():
    bot.set_webhook(f"{DOMAIN}/telegram-hook")
