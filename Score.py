from Utils import BAD_RETURN_CODE, SCORES_FILE_PATH


def read_score(missing_is_zero=True):
    try:
        text = SCORES_FILE_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        if missing_is_zero:
            return 0
        print(f"Error: the score file {SCORES_FILE_PATH} does not exist.")
        return BAD_RETURN_CODE
    except OSError:
        print(f"Error: could not read the score file {SCORES_FILE_PATH}.")
        return BAD_RETURN_CODE
    if not text.isdecimal():
        print(f"Error: the score file {SCORES_FILE_PATH} must contain one non-negative "
              "whole number. The file was left unchanged.")
        return BAD_RETURN_CODE
    return int(text)


def write_score(score):
    try:
        SCORES_FILE_PATH.write_text(str(score), encoding="utf-8")
    except OSError:
        print(f"Error: could not save the score to {SCORES_FILE_PATH}. "
              "The points were not recorded.")
        return False
    return True


def add_score(difficulty):
    current_score = read_score()
    if current_score == BAD_RETURN_CODE:
        return BAD_RETURN_CODE
    POINTS_OF_WINNING = (difficulty * 3) + 5
    new_score = current_score + POINTS_OF_WINNING
    if not write_score(new_score):
        return BAD_RETURN_CODE
    return new_score

