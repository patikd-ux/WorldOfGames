import random


def generate_number(difficulty):
    secret_number = random.randint(1, difficulty)
    return secret_number

