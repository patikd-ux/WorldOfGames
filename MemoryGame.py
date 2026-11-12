import random
import time

from Utils import Screen_cleaner


def generate_sequence(difficulty):
    return [random.randint(1, 101) for _ in range(difficulty)]


def display_sequence(sequence):
    print("Remember this sequence: " + " ".join(str(n) for n in sequence), flush=True)
    time.sleep(0.7)
    Screen_cleaner()


def get_list_from_user(difficulty):
    while True:
        user_input = input(f"Enter the {difficulty} numbers you saw, separated by spaces: ")
        parts = user_input.split()
        if len(parts) != difficulty:
            print(f"Invalid input: please enter exactly {difficulty} numbers.")
            continue
        try:
            return [int(part) for part in parts]
        except ValueError:
            print("Invalid input: please enter whole numbers only, separated by spaces.")


def is_list_equal(list_a, list_b):
    return list_a == list_b


def play(difficulty):
    sequence = generate_sequence(difficulty)
    display_sequence(sequence)
    user_list = get_list_from_user(difficulty)
    result = is_list_equal(sequence, user_list)
    print("The sequence was: " + " ".join(str(n) for n in sequence))
    return result

