import requests

API_KEY = 'bcb0839c86694c4293627019fceb4255'

rates = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + API_KEY).json()['rates']
from_rate = 1 / rates['UAH']

def get_currency(currency, from_num):
    to_rate = rates[currency] * from_rate
    return to_rate * from_num



