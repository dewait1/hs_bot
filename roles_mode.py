from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import test, random, math


def echo(context: CallbackContext, chat_id, text) -> None:
    context.bot.send_message(chat_id = chat_id, text = text)


def new_game(update: Update, players: list) -> None:
    players.clear()

    keyboard = [
        [InlineKeyboardButton("Присоедениться", callback_data = 'new_game')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Новая игра', reply_markup = reply_markup)


def add_player(update: Update, context: CallbackContext, players: list) -> None:
    query = update.callback_query

    new_player = {
        "id" : update.effective_user.id, 
        "name" : update.effective_user.full_name, 
        "role" : ""
    }
    
    if player_in_list(new_player, players):
        return
    else:
        players.append(new_player)
        test.create_players(players)

    answer_text = "Участники:\n"
    index = 1
    for player in players:
        answer_text += str(index) + ". " + player["name"] + "\n"
        index += 1

    query.answer()
    query.edit_message_text(text = answer_text, reply_markup = query.message.reply_markup)


def send_role(update: Update, context: CallbackContext, players: list) -> None:
    query = update.callback_query

    role = next(item for item in players if item["id"] == update.effective_user.id)["role"]

    if role == "Гитлер" : role = "Фашист"

    echo(context, query.data, "Партия игрока " + 
                              update.effective_user.full_name + 
                              ":\n" + 
                              role)

    query.answer()
    query.edit_message_text(text = "Отправлено")


def send_roles(context: CallbackContext, players: list) -> None:
    for player in players:
        context.bot.send_message(chat_id = player["id"], text = "Ты " + player["role"])


def assign_roles(players: list) -> int:
    num = len(players)
    if num > 10 or num < 5: return 0
    
    f = math.floor(num / 2)

    if num % 2 != 1:
        f -= 1

    l = num - f

    randomize_roles(l, f, players)
    return 1


def randomize_roles(num_liberals, num_fascists, players: list) -> None:
    roles = random.sample(["Либерал", "Фашист", "Гитлер"], 
                          counts = [num_liberals, num_fascists - 1, 1], 
                          k = num_liberals + num_fascists)

    for player, role in zip(players, roles):
        player["role"] = role


def show(update: Update, players: list) -> None:
    keyboard = []

    for player in players:
        if update.effective_user.id == player["id"] : continue
        keyboard.append([InlineKeyboardButton(player["name"], callback_data = player["id"])])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Кому?', reply_markup = reply_markup)


def player_in_list(new_player: dict, players: list) -> bool:
    for player in players:
        if new_player["id"] == player["id"]:
            return True
    
    return False