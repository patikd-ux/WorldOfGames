import random

from Utils import get_number_in_range


def generate_number(difficulty):
    secret_number = random.randint(1, difficulty)
    return secret_number


def get_guess_from_user(difficulty):
    return get_number_in_range(f"Guess a number between 1 and {difficulty}: ", 1, difficulty)


def compare_results(guess, secret_number):
    return guess == secret_number


def play(difficulty):
    secret_number = generate_number(difficulty)
    guess = get_guess_from_user(difficulty)
    result = compare_results(guess, secret_number)
    print(f"The secret number was {secret_number}.")
    return result

