from private_variables import BOT_TOKEN
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

board = {
    1: '⬜', 2: '⬜', 3: '⬜',
    4: '⬜', 5: '⬜', 6: '⬜',
    7: '⬜', 8: '⬜', 9: '⬜'}
player = None
computer = None
game_running = True
bot = TeleBot(BOT_TOKEN, parse_mode=None)
temp = None


def is_space_empty(key):
    return board[key] == '⬜'


def insertLetter(letter, position):
    global game_running
    if is_space_empty(position):
        board[position] = letter
    edit_message(temp)
    if check_win(letter):
        bot.delete_message(temp.chat.id, temp.id)
        bot.send_message(temp.chat.id, f"{letter} is win! 🥳 ")
        clear_board()
        game_running = False
    elif checkDraw():
        bot.delete_message(temp.chat.id, temp.id)
        bot.send_message(temp.chat.id, f"DRAW 🤝 ")
        clear_board()
        game_running = False


def check_win(mark):
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    elif board[4] == board[5] and board[4] == board[6] and board[4] == mark:
        return True
    elif board[7] == board[8] and board[7] == board[9] and board[7] == mark:
        return True
    elif board[1] == board[4] and board[1] == board[7] and board[1] == mark:
        return True
    elif board[2] == board[5] and board[2] == board[8] and board[2] == mark:
        return True
    elif board[3] == board[6] and board[3] == board[9] and board[3] == mark:
        return True
    elif board[1] == board[5] and board[1] == board[9] and board[1] == mark:
        return True
    elif board[7] == board[5] and board[7] == board[3] and board[7] == mark:
        return True
    else:
        return False


def checkDraw():
    for key in board.keys():
        if board[key] == '⬜':
            return False
    return True


def clear_board():
    for key in board.keys():
        board[key] = '⬜'


def compMove():
    bestScore = -800
    bestMove = 0
    for key in board.keys():
        if board[key] == '⬜':
            board[key] = computer
            score = minimax(board, False)
            board[key] = '⬜'
            if score > bestScore:
                bestScore = score
                bestMove = key
    insertLetter(computer, bestMove)


def minimax(board, isMaximizing):
    if check_win(computer):
        return 1
    elif check_win(player):
        return -1
    elif checkDraw():
        return 0
    if isMaximizing:
        bestScore = -800
        for key in board.keys():
            if board[key] == '⬜':
                board[key] = computer
                score = minimax(board, False)
                board[key] = '⬜'
                if score > bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 800
        for key in board.keys():
            if board[key] == '⬜':
                board[key] = player
                score = minimax(board, True)
                board[key] = '⬜'
                if score < bestScore:
                    bestScore = score
        return bestScore


def markup():
    global board
    markup_board = InlineKeyboardMarkup(row_width=3)
    _1 = InlineKeyboardButton(text=board[1], callback_data='1')
    _2 = InlineKeyboardButton(text=board[2], callback_data='2')
    _3 = InlineKeyboardButton(text=board[3], callback_data='3')
    _4 = InlineKeyboardButton(text=board[4], callback_data='4')
    _5 = InlineKeyboardButton(text=board[5], callback_data='5')
    _6 = InlineKeyboardButton(text=board[6], callback_data='6')
    _7 = InlineKeyboardButton(text=board[7], callback_data='7')
    _8 = InlineKeyboardButton(text=board[8], callback_data='8')
    _9 = InlineKeyboardButton(text=board[9], callback_data='9')

    markup_board.add(_1, _2, _3,
                     _4, _5, _6,
                     _7, _8, _9)
    return markup_board


def edit_message(message):
    bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=markup())


@bot.message_handler(commands=['start'])
def start(message):
    global game_running
    game_running = True
    clear_board()
    menu = InlineKeyboardMarkup(row_width=2)
    pvp = InlineKeyboardButton(text="Play with Friend 👤", callback_data='pvp')
    pvb = InlineKeyboardButton(text="Play with Bot 🤖", callback_data='pvb')
    menu.add(pvp, pvb)
    bot.send_message(message.chat.id, "Choose one", reply_markup=menu)


@bot.callback_query_handler(func=lambda call: call.data in ['pvp', 'pvb'])
def callback_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == 'pvb':
        choose = InlineKeyboardMarkup(row_width=2)
        _X = InlineKeyboardButton(text='❌', callback_data='❌')
        _0 = InlineKeyboardButton(text='⭕️', callback_data='⭕️')
        choose.add(_X, _0)
        bot.send_message(call.message.chat.id, "Choose your letter", reply_markup=choose)
    else:
        bot.send_message(call.message.chat.id, "Comming soon 😉")


@bot.callback_query_handler(func=lambda call: call.data in ['❌', '⭕️'])
def callback_letter(call):
    global temp
    global computer, player
    bot.delete_message(call.message.chat.id, call.message.id)
    if call.data == '❌':
        player, computer = '❌', '⭕️'
    else:
        player, computer = '⭕️', '❌'
    temp = bot.send_message(call.message.chat.id, "Do something", reply_markup=markup())


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and call.message.id == temp.id)
def update_board(call):
    global board, compMove, temp
    temp = call.message
    key = int(call.data)
    if is_space_empty(key):
        insertLetter(player, key)
        if game_running:
            compMove()
    else:
        bot.answer_callback_query(call.id, text="This spot is not empty", show_alert=True)


bot.infinity_polling()
