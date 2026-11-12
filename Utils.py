import os
from pathlib import Path

# Name of the file that stores the single shared score total.
SCORES_FILE_NAME = "Scores.txt"

# Full path of the score file, shared by the console game and the score service.
# By default it sits in the project folder, no matter which folder the program
# is started from. The container sets WOG_SCORES_FILE=/Scores.txt to use its own file.
SCORES_FILE_PATH = Path(os.environ.get(
    "WOG_SCORES_FILE", Path(__file__).resolve().parent / SCORES_FILE_NAME))

# File that stores each player's score and number of wins (the leaderboard).
PLAYER_SCORES_FILE_NAME = "PlayerScores.json"
PLAYER_SCORES_FILE_PATH = Path(os.environ.get(
    "WOG_PLAYER_SCORES_FILE", Path(__file__).resolve().parent / PLAYER_SCORES_FILE_NAME))

# Returned when reading or writing the score fails.
# A valid score is always a whole number >= 0, so -1 can never be mistaken for one.
BAD_RETURN_CODE = -1


def Screen_cleaner():
    if os.name == "nt":
        os.system("")
    print("\033[H\033[2J\033[3J", end="", flush=True)

