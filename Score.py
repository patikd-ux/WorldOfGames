import json

from Utils import BAD_RETURN_CODE, PLAYER_SCORES_FILE_PATH, SCORES_FILE_PATH


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


def is_valid_player_data(data):
    if not isinstance(data, dict) or not isinstance(data.get("players"), dict):
        return False
    for stats in data["players"].values():
        if not isinstance(stats, dict):
            return False
        for key in ("score", "wins"):
            value = stats.get(key)
            if type(value) is not int or value < 0:
                return False
    return True


def read_player_scores():
    try:
        text = PLAYER_SCORES_FILE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"last_player": None, "players": {}}
    except OSError:
        print(f"Error: could not read the player scores file {PLAYER_SCORES_FILE_PATH}.")
        return None
    try:
        data = json.loads(text)
    except ValueError:
        data = None
    if not is_valid_player_data(data):
        print(f"Error: the player scores file {PLAYER_SCORES_FILE_PATH} is not valid. "
              "The file was left unchanged.")
        return None
    return data


def write_player_scores(data):
    try:
        PLAYER_SCORES_FILE_PATH.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        print(f"Error: could not save the player scores to {PLAYER_SCORES_FILE_PATH}.")
        return False
    return True


def add_player_points(player_name, points):
    data = read_player_scores()
    if data is None:
        return False
    name = player_name.strip() or "Guest"
    stats = data["players"].setdefault(name, {"score": 0, "wins": 0})
    stats["score"] += points
    stats["wins"] += 1
    data["last_player"] = name
    return write_player_scores(data)


def add_score(difficulty, player_name=None):
    current_score = read_score()
    if current_score == BAD_RETURN_CODE:
        return BAD_RETURN_CODE
    POINTS_OF_WINNING = (difficulty * 3) + 5
    new_score = current_score + POINTS_OF_WINNING
    if not write_score(new_score):
        return BAD_RETURN_CODE
    if player_name is not None:
        add_player_points(player_name, POINTS_OF_WINNING)
    return new_score


def get_leaderboard():
    data = read_player_scores()
    if data is None:
        return None
    ranking = sorted(data["players"].items(),
                     key=lambda item: (-item[1]["score"], item[0].lower()))
    rows = [{"rank": rank, "name": name, "score": stats["score"], "wins": stats["wins"]}
            for rank, (name, stats) in enumerate(ranking, start=1)]
    return {"rows": rows, "last_player": data.get("last_player")}
