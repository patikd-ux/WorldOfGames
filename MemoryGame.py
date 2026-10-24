import os
import random
import time


def generate_sequence(difficulty):
    return [random.randint(1, 101) for _ in range(difficulty)]


def clear_screen():
    if os.name == "nt":
        os.system("")
    print("\033[H\033[2J\033[3J", end="", flush=True)


def display_sequence(sequence):
    print("Remember this sequence: " + " ".join(str(n) for n in sequence), flush=True)
    time.sleep(0.7)
    clear_screen()


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

