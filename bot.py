import telebot
from telebot import types
from api import convert_currency, get_currency_rate, params

# Read TOKEN from file
with open("token.txt", "r") as f:
    TOKEN = f.read().rstrip()

# Create the bot
bot = telebot.TeleBot(TOKEN)

# Dictionary of messages thaaat bot can send
# TODO: fill in messages
default_text_messages = {
    "welcome_message": "Я бот ExchangeRate🤖. Мене створили, щоб я допомагав тобі конвертувати валюту та дізнатися поточний курс",
    "help_message": "[throw description]",
    "currency_list": "[currency list]",
    "enter_number": "[enter number in UAH]"
}

# List of available currency
# TODO: fill in the list
list_of_currency = {"AUD": "Австралийский доллар", "ARS": "Аргентинское песо", "BRL": "Бразильский реал",
                    "DKK": "Датская Крона", "USD": "Доллар США", "EUR": "Евро", "ILS": "Израильский шекель",
                    "INR": "Индийская рупия", "IDS": "Индонезийская рупия", "CAD": "Канадский доллар",
                    "CNY": "Китайский юань", "MYR": "Малайзийский ринггит", "MXN": "Мексиканское песо",
                    "NZD": "Новозеландский доллар", "RUB": "Российский рубль", "GBP": "Фунт стерлингов",
                    "TRY": "Турецкая лира", "JPY": "Японская иена"
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

# Creating keyboard markup where user can choose currency (no commands)
# Keyboard Buttons in this markup :
# 1. [USD, --> transfer to handle_currency_exchange()
# TODO: 2. Список валют --> transfer to handle_currency_list_request()
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


# BOT MESSAGE HANDLERS:

# Message handler that handles starting_markup and calls send_help()
def handle_help_request(message):
    if message.text == "Як працює цей бот?":
        send_help(message)


# Message handler that handles request_currency_list_markup and calls send_currency_list()
def handle_currency_list_request(message):
    if message.text == "Список валют":
        send_currency_list(message)


# Message handler that handles currency_list_markup and then sends message asking user to enter his price in UAH
# and parses this price by calling another handler handle_price_request()
def handle_currency_exchange(message):
    text = message.text
    params["to"] = text
    if text in list_of_currency.keys():
        msg = bot.send_message(message.chat.id, default_text_messages["enter_number"])
        bot.register_next_step_handler(msg, handle_price_request)


# Message handler that handles the price entered by user and ...
def handle_price_request(message):
	text = message.text
	if text.isdigit():
		bot.send_message(message.chat.id, "Поточний курс " + list_of_currency[params["to"]] + ": " + str(get_currency_rate(params["to"])))
		bot.send_message(message.chat.id, text + " " + "UAH = " +str(convert_currency(params["to"], text)) + " " + params["to"])
		send_currency_list(message)


# Start the bot polling
bot.infinity_polling()
