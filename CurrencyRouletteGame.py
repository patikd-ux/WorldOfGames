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


def get_money_interval(difficulty, correct_amount):
    margin = Decimal(5 - difficulty)
    return correct_amount - margin, correct_amount + margin


def is_guess_in_interval(guess, interval):
    lower, upper = interval
    return lower <= guess <= upper


def get_guess_from_user(amount):
    while True:
        user_input = input(f"How much is {amount} USD in ILS? ").strip()
        try:
            guess = Decimal(user_input)
        except InvalidOperation:
            print("Invalid input: please enter a number, for example 36 or 36.50.")
            continue
        if not guess.is_finite() or guess < 0:
            print("Invalid input: please enter a non-negative number.")
            continue
        return guess.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def play(difficulty):
    amount = generate_amount()
    rate = get_exchange_rate()
    if rate is None:
        return None
    correct_amount = calculate_ils(amount, rate)
    interval = get_money_interval(difficulty, correct_amount)
    guess = get_guess_from_user(amount)
    result = is_guess_in_interval(guess, interval)
    print(f"The correct value was {correct_amount} ILS (rate: {rate}).")
    return result

