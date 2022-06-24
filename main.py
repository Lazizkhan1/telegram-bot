import telebot
from private_variables import api_key
from currency_module import get_currency
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(api_key, parse_mode=None)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "main menu"),
    telebot.types.BotCommand("/valyuta", "print usage"),
    telebot.types.BotCommand("/help", "print usage")
])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Qelesiz endi ")


@bot.message_handler(commands=['photo'])
def send_welcome(message):
    bot.reply_to(message, "Qelsz endi ")


@bot.message_handler(commands=['creator'])
def send_creator_id(message):
    bot.reply_to(message, "@lazizkhan1")


@bot.message_handler(commands=['valyuta'])
def send_currency(message):
    markup_inline = InlineKeyboardMarkup(row_width=1)
    item_us = InlineKeyboardButton(text="Aqsh Dollar", callback_data='USD')
    item_ru = InlineKeyboardButton(text="Rossiya Rubl", callback_data='RUB')
    markup_inline.add(item_us, item_ru)
    bot.send_message(message.chat.id, "Valyutani tanlang", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def send_currency(call):
    currency = get_currency(call.data)
    bot.send_message(call.message.chat.id,
                     f"Bugungi sana: {currency['date']} \n\n{currency['title']}: {currency['cb_price']} so'm\n")



@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # bot.forward_message(968242298, message.from_user.id, message.id) # you can forward users message to another chat or user
    bot.reply_to(message, message.text)


bot.infinity_polling()
