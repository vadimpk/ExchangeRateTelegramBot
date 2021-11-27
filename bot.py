import telebot
from telebot import types
from api import get_currency

# Read TOKEN from file
with open("token.txt", "r") as f:
    TOKEN = f.read().rstrip()

# Create the bot
bot = telebot.TeleBot(TOKEN)

# Dictionary of messages thaaat bot can send
# TODO: fill in messages
default_text_messages = {
	"welcome_message": "[welcome message]",
	"help_message": "[throw description]",
	"currency_list": "[currency list]",
	"enter_number": "[enter number in UAH]"
}

# List of available currency
# TODO: fill in the list
list_of_currency = ["USD"]

# Creating keyboard markup for transferring user to help message (/help)
# Keyboard Buttons in this markup :
# 1. Як працює цей бот? --> transfer to handle_help_request()
#
# Used in code:
# 1. With /start
starting_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
item = types.KeyboardButton("Як працює цей бот?")
starting_markup.add(item)

# Creating keyboard markup for transferring user to the list of currency (/get_currency_list)
# Keyboard Buttons in this markup :
# 1. Список валют --> transfer to handle_currency_list_request()
#
# Used in code:
# 1. With /help
request_currency_list_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
item = types.KeyboardButton("Список валют")
request_currency_list_markup.add(item)

# Creating keyboard markup where user can choose currency (no commands)
# Keyboard Buttons in this markup :
# 1. [USD, --> transfer to handle_currency_exchange()
# TODO: 2. Список валют --> transfer to handle_currency_list_request()
#
# Used in code:
# 1. With /get_currency_list
currency_list_markup = types.InlineKeyboardMarkup()
item = types.InlineKeyboardButton("USD", callback_data="usd")
currency_list_markup.add(item)

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
	msg = bot.send_message(message.chat.id, default_text_messages["help_message"], reply_markup=request_currency_list_markup)
	bot.register_next_step_handler(msg, handle_currency_list_request)

# Command handler for /start command
# Sends welcome_message and starting_markup where user can choose to see help message
# Call handle_help_request handler after the message
@bot.message_handler(commands=['start'])
def send_welcome(message):
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
	if text in list_of_currency:
		msg = bot.send_message(message.chat.id, default_text_messages["enter_number"])
		#bot.register_next_step_handler(msg, handle_price_request(msg, text))
		bot.register_next_step_handler(msg, handle_price_request(msg, text))

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "usd":
        bot.send_message(call.id, "Answer is Yes")

# Message handler that handles the price entered by user and ...
def handle_price_request(message, c):
	text = message.text
	res = get_currency(c, text)
	bot.send_message(message.chat.id, res)

		# тут треба вже request

# Start the bot polling
bot.infinity_polling()