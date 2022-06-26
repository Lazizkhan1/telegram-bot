from  telebot import TeleBot, types
from private_variables import api_key, video_link
from currency_module import get_currency
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot(api_key, parse_mode=None)
temp = None
last_message = None
bot.set_my_commands([
    types.BotCommand("/start", "Botni ishga tushurish"),
    types.BotCommand("/valyuta", "Valyuta kurslari"),
    types.BotCommand("/game", "Zerkkanla uchun"),
    types.BotCommand("/info", "Bot haqida"),
    types.BotCommand("/help", "Yordam")
])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Qalesiz endi ")\



@bot.message_handler(commands=['valyuta'])
def send_currency(message):
    markup_inline = InlineKeyboardMarkup(row_width=2)
    item_us = InlineKeyboardButton(text="Aqsh Dollar", callback_data='USD')
    item_ru = InlineKeyboardButton(text="Rossiya Rubl", callback_data='RUB')
    markup_inline.add(item_us, item_ru)
    bot.send_message(message.chat.id, "Valyutani tanlang", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'RUB'])
def currency_callback(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    currency = get_currency(call.data)
    bot.send_message(call.message.chat.id,
                     f"Bugungi sana: {currency['date']} \n"
                     f"\n{currency['title']}: {currency['cb_price']} so'm\n")


@bot.callback_query_handler(func=lambda call: call.data in ['🎯', '🎲', '🎳', '🏀', '⚽', '🎰'])
def dice_callback(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, temp.id)
    bot.send_dice(call.message.chat.id, call.data)


@bot.message_handler(commands=['game'])
def send_game(message):
    global temp
    # there sending tutorial video using file_id
    temp = bot.send_video(chat_id=message.chat.id, video=video_link,
                          caption="Qanday o'ynash", supports_streaming=True)
    markup_inline = InlineKeyboardMarkup(row_width=3)
    item_direct_hit = InlineKeyboardButton(text="🎯", callback_data='🎯')
    item_game_die = InlineKeyboardButton(text="🎲", callback_data='🎲')
    item_bowling = InlineKeyboardButton(text="🎳", callback_data='🎳')
    item_basketball = InlineKeyboardButton(text="🏀", callback_data='🏀')
    item_football = InlineKeyboardButton(text="⚽", callback_data='⚽')
    item_slot_machine = InlineKeyboardButton(text="🎰", callback_data='🎰')
    markup_inline.add(item_direct_hit,
                      item_game_die,
                      item_bowling,
                      item_basketball,
                      item_football,
                      item_slot_machine)
    bot.send_message(message.chat.id, "O'yinni tanlang tanlang", reply_markup=markup_inline)


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "*This bot created in 23.06.2022*\n"
                                      "_Bu bot shunchaki tajriba oshirish uchun tuzuldi_.\n"
                                      "*Creator:* @lazizkhan1\n"
                                      "*Tester:* @ellifess\n"
                                      "*Github Link:* https://github.com/Lazizkhan1/telegram-bot",
                     disable_web_page_preview=True, parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def help_(message):
    sent = bot.send_message(message.chat.id, "Shikoyat yoki takliflar bo'lsa yozing!\n"
                                             "yozgan xabaringiz creator ga yuboriladi! ")
    bot.register_next_step_handler(sent, forward_help)


def forward_help(message):
    bot.forward_message(968242298, message.from_user.id, message.id)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "yaxshi " in message.text or "yaxwi " in message.text or "yaxw " in message.text:
        bot.reply_to(message, f"Hardoim yaxshi bo'lin 😊")
    elif "yaxshimas" in message.text or "yaxwimas" in message.text or "yaxwmas" in message.text:
        bot.reply_to(message, f"Bekorlani beshtasini etibsiz, yaxshiku🤪")
    elif "raxmat" in message.text:
        bot.reply_to(message, "Raxmatdan 5 min baqvat 😉")
    elif all(message.text) and message.text[0] == "😂":
        bot.reply_to(message, "🤪")
    elif message.text == "send_photo":
        file = open("test.jpg", "rb")
        bot.send_photo(message.chat.id, file, "This isn't photo")
    else:
        bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
