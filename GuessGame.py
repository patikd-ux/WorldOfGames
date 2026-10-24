import random


def generate_number(difficulty):
    secret_number = random.randint(1, difficulty)
    return secret_number


def get_guess_from_user(difficulty):
    while True:
        user_input = input(f"Guess a number between 1 and {difficulty}: ").strip()
        try:
            guess = int(user_input)
        except ValueError:
            print(f"Invalid input: please enter a whole number between 1 and {difficulty}.")
            continue
        if 1 <= guess <= difficulty:
            return guess
        print(f"Out of range: please enter a number between 1 and {difficulty}.")


def compare_results(guess, secret_number):
    return guess == secret_number


def play(difficulty):
    secret_number = generate_number(difficulty)
    guess = get_guess_from_user(difficulty)
    result = compare_results(guess, secret_number)
    print(f"The secret number was {secret_number}.")
    return result

