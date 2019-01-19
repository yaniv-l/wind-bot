from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import requests
import datetime

from consts import SECRETS
from utils import config



def get_url(station, image):
    # TODO - dynamicly scrap the summery image of wind read from page
    # contents = requests.get('http://wind.co.il/%D7%9E%D7%96%D7%92-%D7%90%D7%95%D7%99%D7%A8/%D7%A9%D7%99%D7%93%D7%95%D7%A8-%D7%97%D7%99/').json()
    # url = contents['url']
    config.get(station, image)
    url = config.get(station, image) + "?t=" + datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    return url


def windalert(bot, update):
    url = get_url("Prigal", "summaryImageURL")
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def sendWindAlert(alert_message):
    updater = Updater(SECRETS.BOTID)
    dp = updater.dispatcher
    dp.bot.send_message(chat_id=SECRETS.CHATID, text=alert_message, parse_mode=ParseMode.MARKDOWN)
    dp.bot.send_photo(chat_id=SECRETS.CHATID, photo=get_url("Prigal", "summaryImageURL"))


def init_bot_listener():
    updater = Updater(SECRETS.BOTID)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('windalert',windalert))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    init_bot_listener()