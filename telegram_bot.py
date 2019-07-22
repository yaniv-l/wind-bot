from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import requests
import datetime

from consts import SECRETS
from utils import config



def get_url(section, image):
    # Get the url for the specific image command - from on config file
    url = None
    if section and image:
        url = config.get(section, image) + "?t=" + datetime.datetime.now().strftime("%d\%m\%Y-%H:%M:%S")

    return url


def windalert(bot, update):
    url = get_url("botimagecommands", update.message.text.replace("/", ""))
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def sendWindAlert(alert_message, sourceName = None):
    updater = Updater(SECRETS.BOTID)
    dp = updater.dispatcher
    dp.bot.send_message(chat_id=SECRETS.CHATID, text=alert_message, parse_mode=ParseMode.MARKDOWN)
    if sourceName:
        image = get_url("botimagecommands", config.get(sourceName, "botSumCmd"))
        if image:
                dp.bot.send_photo(chat_id=SECRETS.CHATID, photo=image)


def init_bot_listener():
    updater = Updater(SECRETS.BOTID)
    dp = updater.dispatcher
    commands = config.options("botimagecommands")
    dp.add_handler(CommandHandler(commands,windalert))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    init_bot_listener()