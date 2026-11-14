import CurrencyRouletteGame
import GuessGame
import MemoryGame
from Score import add_score
from Utils import BAD_RETURN_CODE, get_number_in_range

GAMES = {
    1: MemoryGame,
    2: GuessGame,
    3: CurrencyRouletteGame,
}


def welcome(name):
    return (f"Hello {name} and welcome to the World of Games (WoG).\n"
            "Here you can find many cool games to play.")


def load_game(player_name=None):
    print("Please choose a game to play:")
    print("1. Memory Game - a sequence of numbers will appear for 0.7 seconds "
          "and you have to guess it back")
    print("2. Guess Game - guess a number and see if you chose like the computer")
    print("3. Currency Roulette - try and guess the value of a random amount of USD in ILS")

    game_choice = get_number_in_range("Enter your choice: ", 1, 3)
    difficulty = get_number_in_range("Please choose game difficulty from 1 to 5: ", 1, 5)

    result = GAMES[game_choice].play(difficulty)

    if result is None:
        print("The round was cancelled due to a technical error. No result was recorded.")
    elif result:
        print("Congratulations, you won!")
        new_score = add_score(difficulty, player_name)
        if new_score != BAD_RETURN_CODE:
            print(f"Your total score is now {new_score}.")
    else:
        print("Sorry, you lost. Better luck next time!")

    return result


def main_menu(player_name=None):
    while True:
        print("\nMain Menu:")
        print("1. Enter Games")
        print("2. Exit")
        choice = get_number_in_range("Enter your choice: ", 1, 2)
        if choice == 1:
            load_game(player_name)
        else:
            print("Thank you for playing World of Games. Goodbye!")
            return

