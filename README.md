# World of Games (WoG)

A Python console application with three playable games, a persistent score with a
player leaderboard, and a Flask web service that shows them. Built as a cumulative
DevOps course project.

## Games
1. **Memory Game** - a sequence of numbers appears for 0.7 seconds; repeat it in the same order.
2. **Guess Game** - guess the secret number the computer chose, between 1 and the difficulty.
3. **Currency Roulette** - estimate the ILS value of a random USD amount, using a live exchange rate.

Difficulty ranges from 1 (easiest) to 5 (hardest). Each win adds `(difficulty * 3) + 5`
points (8, 11, 14, 17 or 20) to one shared total. A loss or a cancelled round adds nothing.

## Leaderboard
The same points are also credited to the player who won, by the name entered at the start
of the game. The score page shows a table under the total:

| Column | Meaning |
|---|---|
| Rank | Sorted by score, highest first (ties alphabetically); the top three get 🥇🥈🥉 |
| Player | The name entered at the start (an empty name is stored as `Guest`) |
| Score | All points this player has won |
| Wins | Number of rounds this player has won |

The most recent winner is highlighted with a "last win" tag. If the leaderboard file is
broken, the page still shows the total and says the leaderboard is not available.

## Components
| File | Responsibility |
|---|---|
| `MainGame.py` | Console entry point: asks for the player name and starts the menu |
| `Live.py` | Welcome message, main menu, game selection; awards points after a win |
| `GuessGame.py`, `MemoryGame.py`, `CurrencyRouletteGame.py` | Game logic |
| `Score.py` | Reads and writes the total and the leaderboard; builds the sorted ranking |
| `Utils.py` | Shared settings (file names and paths, `BAD_RETURN_CODE`) and `Screen_cleaner` |
| `MainScores.py` | Flask web service that shows the score and the leaderboard (`templates/score.html`) |
| `Dockerfile`, `docker-compose.yml` | Container image and service for the score page |
| `docker-compose.test.yml` | Test override: mounts the test score file |
| `docker-compose.local.yml` | Local override: mounts the real score and leaderboard files |
| `tests/e2e.py` | Selenium browser test of the score service |

## Requirements
- Python 3.10+
- Internet connection (for Currency Roulette)
- Docker Desktop (for the container)
- Google Chrome (for the browser test; Selenium finds the matching driver itself)

Python dependencies are pinned in `requirements.txt` (`requests`, `Flask`, `selenium` and their dependencies).

## Configuration
| Setting | Value | Where |
|---|---|---|
| Score file name | `Scores.txt` | `Utils.SCORES_FILE_NAME` |
| Leaderboard file name | `PlayerScores.json` | `Utils.PLAYER_SCORES_FILE_NAME` |
| File location | the project folder, whatever folder you start from | `Utils.SCORES_FILE_PATH`, `Utils.PLAYER_SCORES_FILE_PATH` |
| Override the score path | environment variable `WOG_SCORES_FILE` | set to `/Scores.txt` in the `Dockerfile` |
| Override the leaderboard path | environment variable `WOG_PLAYER_SCORES_FILE` | set to `/PlayerScores.json` in the `Dockerfile` |

The score file holds one non-negative whole number. A missing file means a fresh start
(0); an empty, invalid or negative file, or a failed write, is reported as an error and
the file is left unchanged. The leaderboard file follows the same rules: missing means no
players yet, and a broken file is reported and never overwritten.

## How to run
```bash
# 1. Create the virtual environment
py -m venv venv                # Windows
# python3 -m venv venv         # Linux / macOS

# 2. Activate it
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux / macOS

# 3. Install dependencies and play (inside the venv, "python" works on every OS)
pip install -r requirements.txt
python MainGame.py
```

### Score service on your machine
```bash
python MainScores.py           # then open http://localhost:5000
```

### Score service in Docker
```bash
docker compose up -d --build   # then open http://localhost:8777
docker compose down
```

To show your real score and leaderboard in the container, mount them with the local
override (`Scores.txt` and `PlayerScores.json` must exist first, so win at least one round):
```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
docker compose -f docker-compose.yml -f docker-compose.local.yml down
```

## Browser test
The test runs against the container, with a dedicated test score file instead of real game scores:
```bash
docker compose -f docker-compose.yml -f docker-compose.test.yml up -d --build
python tests/e2e.py            # exit code 0 = pass, non-zero = fail
docker compose -f docker-compose.yml -f docker-compose.test.yml down
```
It opens Chrome (headless) at `http://localhost:8777`, waits for the `score` element and
checks that it is a whole number from 1 to 1000. Another URL can be passed as an argument.

## Which files are used where
| Run | Score file | Leaderboard file |
|---|---|---|
| Console game (`python MainGame.py`) | `Scores.txt` in the project folder (not in Git) | `PlayerScores.json` in the project folder (not in Git) |
| Service on your machine (`python MainScores.py`) | the same `Scores.txt`, so a win shows on the next refresh | the same `PlayerScores.json` |
| Container (`docker compose up`) | `/Scores.txt` inside the image, starting at `0` | none, so "No players yet" |
| Container with the local override | your real `Scores.txt`, mounted read-only | your real `PlayerScores.json`, mounted read-only |
| Container for the browser test | `tests/test-score.txt` (`100`), mounted read-only | none |

## Project stages
- [x] **Part 1** - Foundations: console application with three games
- [x] **Part 2** - Scores and containers: score file, leaderboard, Flask service, Docker, Selenium test
- [ ] **Part 3** - External storage, automation and deployment

