import telebot
from currency_module import get_currency

bot = telebot.TeleBot("5522963354:AAG3jgBDTU4hQeq8BJP8BGgtt8rhs8s765A", parse_mode=None)

bot.set_my_commands([
    telebot.types.BotCommand("/start", "main menu"),
    telebot.types.BotCommand("/valyuta", "print usage"),
    telebot.types.BotCommand("/help", "print usage")
])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    bot.reply_to(message, "Qelsz endi ")


@bot.message_handler(commands=['creator', 'admin'])
def send_creator_id(message):
    bot.reply_to(message, "@lazizkhan1")


@bot.message_handler(commands=['valyuta'])
def send_currency(message):
    currency_us = get_currency('USD')
    currency_rub = get_currency('RUB')
    bot.reply_to(message, f"Bugungi sana: {currency_us['date']} \n\n{currency_us['title']}: {currency_us['cb_price']} so'm\n"
                          f"{currency_rub['title']}: {currency_rub['cb_price']} so'm")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()


