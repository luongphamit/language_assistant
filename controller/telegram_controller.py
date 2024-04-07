from datetime import datetime, timedelta
from decimal import Decimal
import json
from locale import currency
import random
from time import sleep, time
from libs.common import CommonLibs
from telegram import ChatMember, ChatMemberUpdated, ParseMode, Update
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
import os
import re
from dateutil.relativedelta import relativedelta
from langdetect import detect
import requests
from dotenv import load_dotenv

load_dotenv()
AZURE_KEY = os.getenv("AZURE_KEY")


class TelegramController:
    def __init__(self, bot, _log) -> None:
        self.common_lib = CommonLibs()
        self.bot = bot
        self._log = _log
        self.switcher = {"translate": self.translate}

    def have_permission(self):
        pass

    def telegram_reply_message(self, update, message, parse_mode=ParseMode.HTML):
        return update.message.reply_text(message, parse_mode=parse_mode)

    def help_command(self, update):
        chat = update.effective_chat
        self.send_message(
            chat.id,
            self.common_lib.get_help_content(update.effective_user.first_name),
            parse_mode=ParseMode.HTML,
        )

    def send_message(
        self, chat_id, message, reply_markup=None, parse_mode=ParseMode.HTML
    ):
        self.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )

    def switch_filter(self, update: Update, context: CallbackContext):
        user = update.effective_user
        user_id = user.id
        chat = update.effective_chat
        group_id = chat.id
        func = self.switcher.get("translate")
        func(update, context)

    def call_api(self, from_lang, to_lang, msg):
        res = requests.post(
            f"https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={from_lang}&to={to_lang}",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                "Ocp-Apim-Subscription-Key": f"{AZURE_KEY}",
                "Ocp-Apim-Subscription-Region": "koreacentral"
            },
            json=[{"Text": msg}]
        )
        if res.status_code == 200:
            data = res.json()
            if len(data):
                return data[0]["translations"][0]["text"]
        return None
        

        # ChatGPT
        # files = {
        #     "file": (None, ""),
        #     "request": (
        #         None,
        #         json.dumps(
        #             {
        #                 "input": msg,
        #                 "source": from_lang,
        #                 "target": to_lang,
        #                 "tool": "ChatGPT",
        #                 "stream": False,
        #             }
        #         ),
        #     ),
        # }
        # res = requests.post(
        #     "https://ai-api.playgroundx.site/translation/translate_long",
        #     headers={
        #         "accept": "application/json",
        #         "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjQ4NTY2ODIxMjQsInVzZXJfaWQiOiIxIn0.4zeYyR-2Y6yhmrk-47eIZpJzJ5fWXyK7tdTmClpoms0"
        #     },
        #     files=files
        # )
        # print(res.text)
        # if res.status_code == 200:
        #     return res.json()["data"]["translation"]

        # return None

    def translate(self, update: Update, context: CallbackContext):
        
        # Translate to ko, vi
        ori_message = update.message.text
        lang = detect(ori_message)
        to_lang = None
        translated = None
        match lang:
            case "vi":
                to_lang = 'ko'
            case "ko":
                to_lang = 'vi'
            case _:
                pass
        if to_lang:
            # Send loading
            msg = context.bot.send_message(update.effective_chat.id, "Translating...")
            translated = self.call_api(lang, to_lang, ori_message)
            if translated:
                new_message = f"""{update.effective_user.first_name}: {translated}"""
                context.bot.edit_message_text(chat_id=update.message.chat_id,
                                    message_id=msg.message_id, 
                                    text=new_message)
            else:
                context.bot.delete_message(msg)
    
    def g_id(self, update: Update, context: CallbackContext):
        self.telegram_reply_message(update=update, message=update.effective_chat.id)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
