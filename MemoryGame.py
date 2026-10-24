import random


def generate_sequence(difficulty):
    return [random.randint(1, 101) for _ in range(difficulty)]

