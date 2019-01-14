from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
import requests
import datetime


def get_url():
    # TODO - dynamicly scrap the summery image of wind read from page
    # contents = requests.get('http://wind.co.il/%D7%9E%D7%96%D7%92-%D7%90%D7%95%D7%99%D7%A8/%D7%A9%D7%99%D7%93%D7%95%D7%A8-%D7%97%D7%99/').json()
    # url = contents['url']
    url = "http://wind.co.il/weather/lab/broadcast.jpg?t=" + datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    return url


def windalert(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def sendWindAlert(alert_message):
    updater = Updater('XXX')
    dp = updater.dispatcher
    dp.bot.send_message(chat_id=XXX, text=alert_message, parse_mode=ParseMode.MARKDOWN)
    dp.bot.send_photo(chat_id=XXX, photo=get_url())


def init_bot_listener():
    updater = Updater('XXX')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('windalert',windalert))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    init_bot_listener()