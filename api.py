import requests

API_KEY = 'bcb0839c86694c4293627019fceb4255'

rates = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + API_KEY).json()['rates']
params = {
    'from' : 'UAH',
    'to': 'USD'
}

from_rate = 1 / rates['UAH']

def convert_currency(currency, from_num):
    to_rate = rates[currency] * from_rate
    return round(to_rate * int(from_num), 2)

def get_currency_rate(currency):
    return round(rates[currency] * from_rate, 2)

