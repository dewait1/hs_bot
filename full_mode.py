from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import test, random


def send_roles_fascists(context: CallbackContext, players: list) -> None:
    fascists = list() 

    message = "Reichstagsgebäude:\n"
    index = 1

    for player in players:
        if player["role"] == "Фашист" or player["role"] == "Гитлер":
            message += "\n" + str(index) + ". " + player["name"] + " - " + player["role"] + "."

            index += 1
            if player["role"] == "Гитлер" and len(players) > 6:
                continue

            fascists.append(player)

    for player in fascists:
        context.bot.send_message(chat_id = player["id"], text = message)



