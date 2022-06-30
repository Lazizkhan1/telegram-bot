import random
import time
from telebot import TeleBot, types
from copy import copy
from private_variables import api_key, video_link, creator_id, tester_id
from currency_module import get_currency
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

bot = TeleBot(api_key, parse_mode=None)
temp_message = None
random_num = [None, None]
count = 0
bot_dice_value = 0
bot.set_my_commands([
    types.BotCommand("/start", "Botni ishga tushurish"),
    types.BotCommand("/valyuta", "Valyuta kurslari"),
    types.BotCommand("/game", "Zerkkanla uchun"),
    types.BotCommand("/info", "Bot haqida"),
    types.BotCommand("/help", "Yordam")
])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Qalesiz endi ")


@bot.message_handler(commands=['valyuta'])
def send_currency(message):
    markup_inline = InlineKeyboardMarkup(row_width=2)
    item_us = InlineKeyboardButton(text="Aqsh Dollar", callback_data='USD')
    item_ru = InlineKeyboardButton(text="Rossiya Rubl", callback_data='RUB')
    markup_inline.add(item_us, item_ru)
    bot.send_message(message.chat.id, "*Valyutani tanlang*\n"
                                      "_Ma'lumotlar NBU bankidan to'g'ridan to'g'ri olinadi!_", parse_mode='Markdown',
                     reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'RUB'])
def currency_callback(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    currency = get_currency(call.data)
    bot.send_message(call.message.chat.id,
                     f"Bugungi sana: {currency['date']} \n"
                     f"\n{currency['title']}: {currency['cb_price']} so'm\n")


@bot.callback_query_handler(func=lambda call: call.data == 'delete-message')
def delete_message(call):
    send_welcome(call.message)
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data in ['🎯', '🎲', '🎳', '🏀', '⚽', '🎰'])
def dice_callback(call):
    global bot_dice_value
    bot.delete_message(call.message.chat.id, call.message.id)
    bot_dice = bot.send_dice(call.message.chat.id, call.data)
    bot_dice_value = bot_dice.dice.value
    bot.reply_to(bot_dice, f"Mani ball'im: *{bot_dice.dice.value}*\nEndi sizni galingiz", parse_mode="Markdown")


@bot.message_handler(content_types=['dice'])
def user_dice_info(message):
    global bot_dice_value
    bot.reply_to(message, f"Sizning ball'ingiz *{message.dice.value}*", parse_mode="Markdown")

    if bot_dice_value == 0:
        dice = bot.send_dice(message.chat.id, message.dice.emoji)
        bot_dice_value = dice.dice.value
        bot.reply_to(dice, f"Mani ball'im: *{dice.dice.value}*", parse_mode="Markdown")
        check_dice(message)
    else:
        check_dice(message)


def check_dice(message):
    global bot_dice_value
    if bot_dice_value > message.dice.value:
        bot.send_message(message.chat.id, "Man yutdim🥳😎")
    elif bot_dice_value < message.dice.value:
        bot.send_message(message.chat.id, "Siz yutdiz🥳😎")
    else:
        bot.send_message(message.chat.id, "Durrang🤝💪")
    bot_dice_value = 0


@bot.message_handler(commands=['game'])
def send_game(message):
    global temp_message
    temp_message = copy(message)
    markup_inline = InlineKeyboardMarkup(row_width=3)
    item_direct_hit = InlineKeyboardButton(text="🎯", callback_data='🎯')
    item_game_die = InlineKeyboardButton(text="🎲", callback_data='🎲')
    item_bowling = InlineKeyboardButton(text="🎳", callback_data='🎳')
    item_basketball = InlineKeyboardButton(text="🏀", callback_data='🏀')
    item_football = InlineKeyboardButton(text="⚽", callback_data='⚽')
    item_slot_machine = InlineKeyboardButton(text="🎰", callback_data='🎰')
    item_guess_number = InlineKeyboardButton(text="Yashirin Son", callback_data='gn')
    markup_inline.add(item_direct_hit,
                      item_game_die,
                      item_bowling,
                      item_basketball,
                      item_football,
                      item_slot_machine,
                      item_guess_number)
    bot.send_video(chat_id=message.chat.id, video=video_link,
                   caption="*O'YINNI O'YNASHDAN OLDIN BU VIDEONI KO'RING* \n\nO'yinlardan birini tanlang",
                   parse_mode='Markdown',
                   supports_streaming=True, reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data == 'gn')
def guess_number(call):
    global temp_message
    temp_message = call.data
    bot.delete_message(call.message.chat.id, call.message.id)
    markup_inline = InlineKeyboardMarkup(row_width=1)
    item_hard = InlineKeyboardButton(text="Qiyin", callback_data='gn_hard')
    item_medium = InlineKeyboardButton(text="O'rtacha", callback_data='gn_medium')
    item_easy = InlineKeyboardButton(text="Oson", callback_data='gn_easy')
    markup_inline.add(item_hard, item_medium, item_easy)
    bot.send_message(call.message.chat.id, "O'yinni qiyinligini tanlang", reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: call.data in ['gn_hard', 'gn_medium', 'gn_easy'])
def gn_set_difficulty(call):
    global random_num
    to = 0
    if call.data == 'gn_hard':
        to = 100
    elif call.data == 'gn_medium':
        to = 50
    else:
        to = 20
    random_num[1] = to
    random_num[0] = random.randint(1, to)
    print(random_num[0])
    bot.send_message(call.message.chat.id, f"*1* dan *{to}* gacha bolgan sonlar ichidan yashirin sonni toping.\n"
                                           f"_Iltimos biror son kiriting_.\n", parse_mode='Markdown')
    bot.register_next_step_handler(call.message, guess_number_game)
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.message_handler(func=lambda message: temp_message == "gn")
def guess_number_game(message):
    global random_num, count, temp_message
    if message.text.isnumeric():
        user_guess = int(message.text)
        if user_guess in range(1, random_num[1] + 1):
            if user_guess > random_num[0]:
                count += 1
                bot.send_message(message.chat.id, "Kichikroq son kiriting")
            elif user_guess < random_num[0]:
                count += 1
                bot.send_message(message.chat.id, "Kattaroq son kiriting")
            else:
                bot.send_message(message.chat.id, f"*Topdingiz* 🥳😎 \n"
                                                  f"*Yashirin son*: {random_num[0]} \n"
                                                  f"*Urunishlar soni*: {count + 1} ta \n",
                                                  parse_mode="Markdown")
                temp_message = None
                count = 0
                retry_game(message)
        else:
            bot.send_message(message.chat.id, f"1 va {random_num[1]} orasidagi sonlarni kiriting!")
    else:
        bot.send_message(message.chat.id, "Iltimos faqat son kiriting!")


def retry_game(message):
    markup_inline = InlineKeyboardMarkup(row_width=2)
    item_yes = InlineKeyboardButton(text="Ha", callback_data='gn')
    item_no = InlineKeyboardButton(text="Yo'q", callback_data='delete-message')
    markup_inline.add(item_yes, item_no)
    bot.send_message(message.chat.id, "Yana o'ynaysizmi?", reply_markup=markup_inline)


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.send_message(message.chat.id, "*This bot created in 23.06.2022*\n"
                                      "_Bu bot shunchaki tajriba oshirish uchun tuzuldi_.\n"
                                      "*Creator:* @lazizkhan1\n"
                                      "*Assistant:* @ellifess\n"
                                      "*Github Link:* https://github.com/Lazizkhan1/telegram-bot",
                                      disable_web_page_preview=True, parse_mode="Markdown")


@bot.message_handler(commands=['help'])
def help_(message):
    sent = bot.send_message(message.chat.id, "Shikoyat yoki takliflar bo'lsa yozing!\n"
                                             "yozgan xabaringiz creator ga yuboriladi! ")
    bot.register_next_step_handler(sent, forward_help)


def forward_help(message):
    bot.forward_message(creator_id, message.from_user.id, message.id)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    msg = message.text.strip().lower()
    if "yaxshi" == msg or "yaxwi " == msg or "yaxw " == msg:
        bot.reply_to(message, f"Hardoim yaxshi bo'lin 😊")
    elif "yaxshimas" in msg or "yaxwimas" in msg or "yaxwmas" in msg:
        bot.reply_to(message, f"Bekorlani beshtasini etibsiz, yaxshiku 🤪")
    elif "raxmat" in msg:
        bot.reply_to(message, "Raxmatdan 5 min baqvat 😉")
    elif "hop" in msg:
        bot.reply_to(message, "Malades, o'zim orgili hop dgan so'zizdan 😊")
    elif "chiki chiki" == msg or "ciki ciki" == msg:
        bot.reply_to(message, "Iltimos sof o'zbek tilidan foydalaning! 😉")
    elif "yo'q" in msg or "yoq" in msg:
        bot.reply_to(message, "Yo'q diyish 15 min 😂")
    elif "muncha" in msg or "buncha" in msg:
        bot.reply_to(message, "Shunaqadee endi 😊")
    elif all(msg) and msg[0] == "😂":
        bot.reply_to(message, "🤪")
    else:
        bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
