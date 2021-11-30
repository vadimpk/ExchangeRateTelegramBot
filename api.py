"""
api.py
file that uses openexchangerates.org API to exchange currency rates
"""
import requests

# Read TOKEN from file
with open("api_token.txt", "r") as f:
    API_TOKEN = f.read().rstrip()

# make request
rates = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + API_TOKEN).json()['rates']

from_rate = 1 / rates['UAH']

# Method that converts given sum of money from UAH into given currency
def convert_currency(currency, from_num):
    to_rate = rates[currency] * from_rate
    return round(to_rate * int(from_num), 2)

# Method that calculates rate from UAH into given currency
def get_currency_rate(currency):
    return round(rates[currency] * from_rate, 2)

