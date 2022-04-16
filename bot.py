import logging
import core, t
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters


players = []

# Logging enabling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def msg(update: Update, context: CallbackContext, text: str) -> None:
    update.message.reply_markup = ReplyKeyboardRemove
    core.echo(context, update.effective_chat.id, text)


def start(update: Update, context: CallbackContext) -> None:
    msg(update, context, "Cierć!")


def new_game(update: Update, context: CallbackContext) -> None:
    if update.effective_chat.type != 'group':
        msg(update, context, 'Игра может быть начата только в групповом чате')
        return
        
    core.new_game(update, players)


def join_button(update: Update, context: CallbackContext) -> None:
    if update.callback_query.data == 'new_game':
        core.add_player(update, context, players) 
    else:
        core.send_role(update, context, players)


def start_game(update: Update, context: CallbackContext) -> None: 
    if update.effective_chat.type != 'group':
        return
    
    if core.assign_roles(players) == 0:
        msg(update, context, "Неподходящее кол-во игроков")
        return
    
    core.send_roles(context, players)

    msg(update, context, "Игра началась!")


def show_button(update: Update, context: CallbackContext) -> None:
    if len(players) < 5:
        msg(update, context, "Еблан?")
        return

    core.show(update, players)


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