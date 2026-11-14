import json

import pytest

import Score
from Utils import BAD_RETURN_CODE


@pytest.fixture
def files(tmp_path, monkeypatch):
    # Point Score.py at empty files in a temporary folder: real scores are never touched.
    score_file = tmp_path / "Scores.txt"
    players_file = tmp_path / "PlayerScores.json"
    monkeypatch.setattr(Score, "SCORES_FILE_PATH", score_file)
    monkeypatch.setattr(Score, "PLAYER_SCORES_FILE_PATH", players_file)
    return score_file, players_file


# ---------- total score (spec tasks 2-3) ----------

@pytest.mark.parametrize("difficulty, points", [(1, 8), (2, 11), (3, 14), (4, 17), (5, 20)])
def test_first_win_creates_file_with_points(files, difficulty, points):
    score_file, _ = files
    assert Score.add_score(difficulty) == points
    assert score_file.read_text(encoding="utf-8") == str(points)


def test_spec_example_20_plus_difficulty_3_is_34(files):
    score_file, _ = files
    score_file.write_text("20", encoding="utf-8")
    assert Score.add_score(3) == 34
    assert Score.read_score() == 34


def test_second_win_adds_to_saved_total(files):
    Score.add_score(1)
    assert Score.add_score(1) == 16


def test_missing_file_is_zero_for_game_and_error_for_service(files):
    assert Score.read_score() == 0
    assert Score.read_score(missing_is_zero=False) == BAD_RETURN_CODE


@pytest.mark.parametrize("content", ["", "abc", "-5", "1.5"])
def test_invalid_file_is_reported_and_left_unchanged(files, content):
    score_file, _ = files
    score_file.write_text(content, encoding="utf-8")
    assert Score.add_score(3) == BAD_RETURN_CODE
    assert score_file.read_text(encoding="utf-8") == content


def test_failed_write_keeps_the_old_score(files):
    score_file, _ = files
    score_file.write_text("34", encoding="utf-8")
    # A folder with the side file's name makes the write fail.
    score_file.with_name(score_file.name + ".tmp").mkdir()
    assert Score.add_score(3) == BAD_RETURN_CODE
    assert score_file.read_text(encoding="utf-8") == "34"


# ---------- leaderboard (addition beyond the spec) ----------

def test_leaderboard_ranks_by_score_then_name(files):
    Score.add_score(5, "Daniel")
    Score.add_score(3, "Noa")
    Score.add_score(3, "Avi")
    board = Score.get_leaderboard()
    assert [(row["rank"], row["name"], row["score"]) for row in board["rows"]] == [
        (1, "Daniel", 20), (2, "Avi", 14), (3, "Noa", 14)]
    assert board["last_player"] == "Avi"


def test_wins_are_counted_per_player(files):
    Score.add_score(1, "Noa")
    Score.add_score(2, "Noa")
    row = Score.get_leaderboard()["rows"][0]
    assert (row["name"], row["score"], row["wins"]) == ("Noa", 19, 2)


def test_blank_name_is_guest_and_no_name_is_total_only(files):
    Score.add_score(1, "   ")
    Score.add_score(1)
    assert Score.read_score() == 16
    assert [row["name"] for row in Score.get_leaderboard()["rows"]] == ["Guest"]


def test_broken_leaderboard_never_blocks_the_total(files):
    score_file, players_file = files
    broken = json.dumps({"players": {"Noa": {"score": True, "wins": 1}}})
    players_file.write_text(broken, encoding="utf-8")
    assert Score.add_score(3, "Noa") == 14
    assert Score.get_leaderboard() is None
    assert players_file.read_text(encoding="utf-8") == broken

