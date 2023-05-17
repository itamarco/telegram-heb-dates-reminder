import telebot
from date_utils import heb_date_str_to_hebrew_date
from text_patterns import is_date_msg

TELEGRAM_TOKEN = '5029905616:AAFsTd-gIiLF_f0IqftNgENqkfqF4d9xwGM'

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@bot.message_handler(commands=["hello"])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Hello Friend!")


@bot.message_handler(commands=["start"])
def handle_new_chat_member(message):
    chat_id = message.chat.id

    # Create a custom keyboard with options
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add('Option 1', 'Option 2')
    keyboard.add('Option 3', 'Option 4')

    # Send a welcome message with the custom keyboard
    bot.send_message(chat_id, "Welcome! Please choose an option:", reply_markup=keyboard)


@bot.message_handler(func=lambda msg: is_date_msg(msg.text))
def handle_date(message):
    date = heb_date_str_to_hebrew_date(message.text)
    bot.send_message(message.chat.id, date.hebrew_date_string())


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)
