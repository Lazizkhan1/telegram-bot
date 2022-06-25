import telebot
from private_variables import api_key
from currency_module import get_currency
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(api_key, parse_mode=None)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "Botni ishga tushurish"),
    telebot.types.BotCommand("/valyuta", "Valyuta kurslari"),
    telebot.types.BotCommand("/info", "Bot haqida"),
    telebot.types.BotCommand("/help", "Yordam")
])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Qelesiz endi ")


@bot.message_handler(commands=['valyuta'])
def send_currency(message):
    markup_inline = InlineKeyboardMarkup(row_width=2)
    item_us = InlineKeyboardButton(text="Aqsh Dollar", callback_data='USD')
    item_ru = InlineKeyboardButton(text="Rossiya Rubl", callback_data='RUB')
    markup_inline.add(item_us, item_ru)
    bot.send_message(message.chat.id, "Valyutani tanlang", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback_currency(call):
    currency_list = ['USD', 'RUB']
    if call.data in currency_list:
        bot.delete_message(call.message.chat.id, call.message.id)
        currency = get_currency(call.data)
        bot.send_message(call.message.chat.id,
                         f"Bugungi sana: {currency['date']} \n"
                         f"\n{currency['title']}: {currency['cb_price']} so'm\n")


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "This bot created in 23.06.2022\n"
                                      "Bu bot shunchaki tajriba oshirish uchun tuzuldi."
                                      "Creator: @lazizkhan1\n"
                                      "Tester: @ellifess\n"
                                      "Github Link: https://github.com/Lazizkhan1/telegram-bot",
                     disable_web_page_preview=True)


@bot.message_handler(commands=['help'])
def help_(message):
    sent = bot.send_message(message.chat.id, "Shikoyat yoki takliflar bo'lsa yozing!\n"
                                             "yozgan xabaringiz creator ga yuboriladi! ")
    bot.register_next_step_handler(sent, forward_help)


def forward_help(message):
    bot.forward_message(968242298, message.from_user.id, message.id)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.from_user.id != 968242298:
        bot.forward_message(968242298, message.from_user.id, message.id)
        # you can forward users message to another chat or user
        bot.reply_to(message, message.text)
    if "yaxshi" in message.text or "yaxwi" in message.text or "yaxw" in message.text:
        bot.reply_to(message, f"Hardoim yaxshi bo'lin 😊")
    elif "raxmat" in message.text:
        bot.reply_to(message, "Raxmatdan 5 min baqvat 😉")
    elif all(message.text) and message.text[0] == "😂":
        bot.reply_to(message, "🤪")
    else:
        bot.reply_to(message, message.text)


bot.infinity_polling()
