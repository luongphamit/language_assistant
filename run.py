from datetime import datetime, time, timedelta
from email import message
from functools import wraps
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    ChatMemberHandler,
    ConversationHandler,
    CallbackQueryHandler,
)
from dotenv import load_dotenv
import os
import telegram
import json
from controller.telegram_controller import TelegramController
from libs.common import CommonLibs
from models.logger import Log
import pytz

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL")

signal = ""
_common = CommonLibs()
_log = Log(f"{os.path.dirname(os.path.abspath(__file__))}/logs/bot.log", LOG_LEVEL)
telegram_bot = telegram.Bot(BOT_TOKEN)
__telegram_controller = TelegramController(telegram_bot, _log)


def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context, *args, **kwargs):
        if update.effective_chat.id in [-1002073035751]:
            return func(update, context, *args, **kwargs)
        
        return

    return wrapped


@restricted
def start_command(update: Update, context: CallbackContext) -> None:
    __telegram_controller.telegram_reply_message(
        update, "Welcome, /help to show how to use"
    )
    
@restricted
def help_command(update: Update, context: CallbackContext) -> None:
    __telegram_controller.help_command(update)

@restricted
def msg_filter_command(update: Update, context: CallbackContext) -> None:
    __telegram_controller.switch_filter(update, context)
    
def g_id(update: Update, context: CallbackContext) -> None:
    __telegram_controller.g_id(update, context)



def main() -> None:

    updater = Updater(BOT_TOKEN, workers=32)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("g_id", g_id))
    dispatcher.add_handler(MessageHandler(Filters.all, msg_filter_command, run_async=True))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()


if __name__ == "__main__":
    main()
