import logging
import roles_mode, t, full_mode
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

players = []

# Logging enabling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def msg(update: Update, context: CallbackContext, text: str) -> None:
    update.message.reply_markup = ReplyKeyboardRemove
    roles_mode.echo(context, update.effective_chat.id, text)


def start(update: Update, context: CallbackContext) -> None:
    msg(update, context, "Cierć!")


def new_game(update: Update, context: CallbackContext) -> None:    
    roles_mode.new_game(update, players)


def join_button(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'new_game':
        roles_mode.add_player(update, context, players) 
    else:
        roles_mode.send_role(update, context, players)


def start_game(update: Update, context: CallbackContext) -> None: 
    if roles_mode.assign_roles(players) == 0:
        msg(update, context, "Неподходящее кол-во игроков")
        return
    
    roles_mode.send_roles(context, players)
    full_mode.send_roles_fascists(context, players)

    msg(update, context, "Игра началась!")


def show_button(update: Update, context: CallbackContext) -> None:
    if len(players) < 5:
        msg(update, context, "Еблан?")
        return

    roles_mode.show(update, players)


def main() -> None:
    updater = Updater(t.get_token())

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(join_button))
    updater.dispatcher.add_handler(CommandHandler('newgame', new_game))
    updater.dispatcher.add_handler(CommandHandler('startgame', start_game))
    updater.dispatcher.add_handler(CommandHandler('show', show_button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), msg))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()