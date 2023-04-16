import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler
from telegram.ext.filters import Filters  # pip install python-telegram-bot

data = {}
logs = {}
users = {
    6092106007: [{
        "name" : " Видеокарта Afox Radeon RX 550 4Gb AFRX550-4096D5H4-V4",
        "price": 8321,
        "link" : "https://quke.ruhttps://quke.ru/shop/UID_103396__afox_radeon_rx_550_4gb_afrx5504096d5h4v4.html"
    }, {
        "name" : " Видеокарта Afox Radeon RX 550 4Gb AFRX550-4096D5H4-V4",
        "price": 8321,
        "link" : "https://quke.ruhttps://quke.ru/shop/UID_103396__afox_radeon_rx_550_4gb_afrx5504096d5h4v4.html"
    }, {
        "name" : " Видеокарта Afox Radeon RX 550 4Gb AFRX550-4096D5H4-V4",
        "price": 8321,
        "link" : "https://quke.ruhttps://quke.ru/shop/UID_103396__afox_radeon_rx_550_4gb_afrx5504096d5h4v4.html"
    }]
}


def start(update: Update, context: CallbackContext):
    update.message.reply_text('👋Привет!')
    update.message.reply_text('Этот бот создал для облегчения жизни людям которые хотят собрать компьютер \n\n<b>Инструкция: </b>'
                              '\n /set - посмотреть текущею сборку'
                              '\n /search (текст) - найти комплектующи', parse_mode='html')


def catalog(update: Update, context: CallbackContext):
    msg = '<b>🛠 Ваша Сборка: </B>\n'
    print(update.message.from_user.id)
    mark = users.get(update.message.from_user.id)
    if not mark:
        msg += '\n У вас пока сборка пустая('
    else:
        sum_mark = 0
        for n, i in enumerate(mark, 1):
            msg += f'\n<b>{n})</b> {i["price"]:,} ₽: <a href="{i["link"]}">{i["name"]}</a>'
            sum_mark += i['price']
        msg += f'\n\n<b>Total: </b> {sum_mark:,} руб'
    update.message.reply_text(msg, parse_mode='HTML')


def get_query(update: Update, context: CallbackContext):
    pass


def log(update: Update, context: CallbackContext):
    update.message.reply_text(str(logs))


def update_db():
    global shop, users
    json.dump({'shop': shop, 'users': users}, open('bd.json', 'w'))


def get_db():
    global data
    data = {
        'card'       : [],
        'processor'  : [],
        'motherboard': [],
        'RAM'        : [],
        'power'      : [],
        'memory'     : [],
    }

    for i in ['quke']:
        db = json.load(open('bd.json'))
        for i in data:
            type = db.get(i)
            if type:
                data[i].extend(type)


def main():
    updater = Updater("6052987327:AAEJvciuYT7b8DWgujvx9yJRoV_6EFuzMbU", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', start))
    dp.add_handler(CommandHandler('set', catalog))
    dp.add_handler(CommandHandler('log', log))
    dp.add_handler(CallbackQueryHandler(get_query))
    print('ready')
    updater.start_polling()
    updater.idle()


main()