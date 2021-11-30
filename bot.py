"""
EXCHANGE RATE BOT TELEGRAM
Test project for @Vstup_NaUKMA_bot team
Authors:
    Vadym Polishchuk @vadimpk
    Stanislav Bukovskiy @ shablavuuu
Task: to create a simple telegram bot that can convert sum in UAH into any other currency (using real-time data)
"""

import telebot
from telebot import types
from api import convert_currency, get_currency_rate

# Read TOKEN from file
with open("token.txt", "r") as f:
    TOKEN = f.read().rstrip()

# Create the bot
bot = telebot.TeleBot(TOKEN)

# dictionary of users to store currency they are working with
# key: user chat.id
# value: current currency
user_currency = {}

# List of available currency
list_of_currency = {"AUD": "Австралійський долар", "ARS": "Аргентинське песо", "BRL": "Бразильський реал",
                    "DKK": "Данська крона", "USD": "Долар США", "EUR": "Євро", "ILS": "Ізраїльський шекель",
                    "INR": "Індійська рупія", "IDS": "Індонезійська рупія", "CAD": "Канадський долар",
                    "CNY": "Китайський юань", "MYR": "Малайзійський рингіт", "MXN": "Мексиканський песо",
                    "NZD": "Новозеландський долар", "RUB": "Російський рубль", "GBP": "Фунт стерлінгів",
                    "TRY": "Турецька ліра", "JPY": "Японська єна"
                    }

# Converting currency list into readable message
def currency_list_to_message(dict):
    message = ""
    for currency_code in dict:
        message = message + currency_code + " - " + dict[currency_code] + "\n"
    return message

# Dictionary of messages that bot can send
default_text_messages = {
    "welcome_message": "Я бот ExchangeRate🤖. Мене створили, щоб я допомагав тобі конвертувати валюту та дізнатися поточний курс",
    "help_message": "Я можу конвертувати будь-яку суму в гривнях в іншу валюту зі списку валют. Виберіть потрібну валюту та введіть суму в гривнях, щоб отримати результат \n /get_currency_list переглянути список валют",
    "currency_list": currency_list_to_message(list_of_currency),
    "enter_number": "Введіть суму в гривнях",
    "currency_not_found": "На жаль, такої валюти немає, спробуйте ще раз",
    "incorrect_number": "Ви ввели недійсне число",
    "cant_recognize_text": "Упс, не можу розпізнати ваше повідомлення"
}

# Creating keyboard markup for transferring user to help message (/help)
# Keyboard Buttons in this markup :
# 1. Як працює цей бот? --> transfer to handle_help_request()
#
# Used in code:
# 1. With /start
starting_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item = types.KeyboardButton("Як працює цей бот?")
starting_markup.add(item)

# Creating keyboard markup for transferring user to the list of currency (/get_currency_list)
# Keyboard Buttons in this markup :
# 1. Список валют --> transfer to handle_currency_list_request()
#
# Used in code:
# 1. With /help
request_currency_list_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
item = types.KeyboardButton("Список валют")
request_currency_list_markup.add(item)

# Creating keyboard markup where user can choose currency
# Keyboard Buttons in this markup :
# All elements from list_of_currency
#
# Used in code:
# 1. With /get_currency_list
currency_list_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
currency_list_markup.row(*list(list_of_currency.keys())[:6])
currency_list_markup.row(*list(list_of_currency.keys())[6:12])
currency_list_markup.row(*list(list_of_currency.keys())[12:])


# BOT COMMAND HANDLERS:

# Command handler for /get_currency_list command
# Sends currency_list and currency_list_markup where user can choose his currency or go back to currency list
# Call handle_currency_exchange handler after the message
@bot.message_handler(commands=['get_currency_list'])
def send_currency_list(message):
    msg = bot.send_message(message.chat.id, default_text_messages["currency_list"], reply_markup=currency_list_markup)
    bot.register_next_step_handler(msg, handle_currency_exchange)


# Command handler for /help command
# Sends help_message and request_currency_list_markup where user can choose to see currency list
# Call handle_currency_list_request handler after the message
@bot.message_handler(commands=['help'])
def send_help(message):
    msg = bot.send_message(message.chat.id, default_text_messages["help_message"],
                           reply_markup=request_currency_list_markup)
    bot.register_next_step_handler(msg, handle_currency_list_request)

# Command handler for /start command
# Sends welcome_message and starting_markup where user can choose to see help message
# Call handle_help_request handler after the message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привіт, " + message.from_user.username + "👋", reply_markup=starting_markup)
    msg = bot.send_message(message.chat.id, default_text_messages["welcome_message"], reply_markup=starting_markup)
    bot.register_next_step_handler(msg, handle_help_request)

# Command handler for currency
# If user types currency in chat, it runs
@bot.message_handler(func=lambda message: message.text in list_of_currency.keys())
def handle_random_currency_request(message):
    user_currency[message.chat.id] = message.text
    msg = bot.send_message(message.chat.id, default_text_messages["enter_number"])
    bot.register_next_step_handler(msg, handle_price_request)

# BOT MESSAGE HANDLERS:

# Message handler that handles starting_markup and calls send_help()
def handle_help_request(message):
    if message.text == "Як працює цей бот?":
        send_help(message)
    elif message.text == "/get_currency_list":
        send_currency_list(message)
    else:
        bot.send_message(message.chat.id, default_text_messages["cant_recognize_text"])


# Message handler that handles request_currency_list_markup and calls send_currency_list()
def handle_currency_list_request(message):
    if message.text == "Список валют":
        send_currency_list(message)
    else:
        bot.send_message(message.chat.id, default_text_messages["cant_recognize_text"])


# Message handler that handles currency_list_markup and then sends message asking user to enter his price in UAH
# and parses this price by calling another handler handle_price_request()
def handle_currency_exchange(message):
    currency = message.text
    if currency in list_of_currency.keys():
        user_currency[message.chat.id] = currency
        msg = bot.send_message(message.chat.id, default_text_messages["enter_number"])
        bot.register_next_step_handler(msg, handle_price_request)
    elif currency == "/start":
        send_welcome(message)
    elif currency == "/help":
        send_help(message)
    elif text == "/get_currency_list":
        send_currency_list(message)
    else:
        bot.send_message(message.chat.id, default_text_messages["currency_not_found"])
        send_currency_list(message)


# Message handler that handles the price entered by user and shows the result of converting
# After calls send_currency_list()
def handle_price_request(message):
    text = message.text
    if text.isdigit():
        bot.send_message(message.chat.id, "Поточний курс " + list_of_currency[user_currency[message.chat.id]] + ": " + str(get_currency_rate(user_currency[message.chat.id])))
        bot.send_message(message.chat.id, text + " " + "UAH = " +str(convert_currency(user_currency[message.chat.id], text)) + " " + user_currency[message.chat.id])
        send_currency_list(message)
    elif text == "/start":
        send_welcome(message)
    elif text == "/help":
        send_help(message)
    elif text == "/get_currency_list":
        send_currency_list(message)
    else:
        bot.send_message(message.chat.id, default_text_messages["incorrect_number"])
        send_currency_list(message)

# Start the bot polling
bot.infinity_polling()
