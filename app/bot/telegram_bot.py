from app.bot.bot_impl import BotImpl, callback_action_delimiter
from app.user_flow import parse_freetext_input, handle_callback_actions

heb_date_bot = BotImpl()
bot = heb_date_bot.get_bot()


@bot.message_handler(commands=["start"])
def handle_new_chat_member(message):
    chat_id = message.chat.id
    heb_date_bot.send_menu_keyboard(chat_id)


@bot.message_handler(content_types=['new_chat_members'])
def handle_new_chat_member(message):
    chat_id = message.chat.id
    heb_date_bot.send_menu_keyboard(chat_id)


@bot.message_handler(func=lambda message: message.text == "התחל")
def parse_with_context(message):
    chat_id = message.chat.id
    heb_date_bot.send_menu_keyboard(chat_id)


@bot.message_handler(func=lambda message: True)
def parse_with_context(message):
    user_id = chat_id = message.chat.id
    response = parse_freetext_input(user_id, message.text)
    if response.items_display:
        heb_date_bot.send_inline_buttons(chat_id, response.text,
                                         items_display=response.items_display,
                                         items_callback_data=response.items_callback_data,
                                         action=response.action)
    else:
        heb_date_bot.send_msg(chat_id, response.text)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = chat_id = call.message.chat.id
    delimiter = callback_action_delimiter

    # 'call.data' contains the value that was sent back to the bot when the item was clicked
    action, data = call.data.split(delimiter)
    response = handle_callback_actions(user_id, action, data)
    heb_date_bot.send_msg(chat_id, response.text)
