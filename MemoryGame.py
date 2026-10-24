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

