import random
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import requests

API_URL = "https://open.er-api.com/v6/latest/USD"


def generate_amount():
    return random.randint(1, 100)


def get_exchange_rate(url=API_URL):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        rate = Decimal(str(response.json()["rates"]["ILS"]))
    except (requests.RequestException, ValueError, KeyError, TypeError, InvalidOperation):
        print("Error: could not retrieve the USD to ILS exchange rate. The round is cancelled.")
        return None
    if rate <= 0:
        print("Error: received an invalid exchange rate. The round is cancelled.")
        return None
    return rate


def calculate_ils(amount, rate):
    return (Decimal(amount) * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

