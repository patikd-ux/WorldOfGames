# World of Games (WoG)

Flask web service that shows the score. Built as a cumulative DevOps course project.

## Games
1. **Memory Game** - a sequence of numbers appears for 0.7 seconds; repeat it in the same order.
3. **Currency Roulette** - estimate the ILS value of a random USD amount, using a live exchange rate.

Difficulty ranges from 1 (easiest) to 5 (hardest). Each win adds `(difficulty * 3) + 5`

## Components
| File | Responsibility |
|---|---|
| `MainGame.py` | Console entry point |
| `Live.py` | Welcome message, main menu, game selection; awards points after a win |
| `GuessGame.py`, `MemoryGame.py`, `CurrencyRouletteGame.py` | Game logic |
| `Utils.py` | Shared settings (`SCORES_FILE_NAME`, score file path, `BAD_RETURN_CODE`) and `Screen_cleaner` |
| `MainScores.py` | Flask web service that shows the current score (`templates/score.html`) |
| `Dockerfile`, `docker-compose.yml` | Container image and startup for the score service |
| `tests/e2e.py` | Selenium browser test of the score service |
| `docker-run-command.txt` | Short startup notes and a direct `docker run` command |

- Python 3.10+
- Internet connection (for Currency Roulette)
- Google Chrome (for the browser test; Selenium finds the matching driver itself)

Python dependencies are pinned in `requirements.txt` (`requests`, `Flask`, `selenium` and their dependencies).
## Configuration
| Setting | Value | Where |
|---|---|---|
| Score file name | `Scores.txt` | `Utils.SCORES_FILE_NAME` |
| Score file path | the project folder, whatever folder you start from | `Utils.SCORES_FILE_PATH` |
| Service port | `5000` inside, `8777` on the host | `MainScores.PORT`, `docker-compose.yml` |

The score file holds one non-negative whole number. A missing file means a fresh start
the file is never overwritten.

## How to run
```bash
# 1. Create the virtual environment
py -m venv venv                # Windows
# python3 -m venv venv         # Linux / macOS

# 2. Activate it
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
python MainGame.py
```

### Score service on your machine
```bash
python MainScores.py           # then open http://localhost:5000

### Score service in Docker
```bash
docker compose up -d --build   # then open http://localhost:8777
docker compose down
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

## Which score file is used where
| Run | Score file |
|---|---|
| Console game (`python MainGame.py`) | `Scores.txt` in the project folder (not in Git) |
| Service on your machine (`python MainScores.py`) | the same `Scores.txt`, so a win shows on the next refresh |
| Container (`docker compose up`) | `/Scores.txt` inside the image, starting at `0` |
| Container for the browser test | `tests/test-score.txt` (`100`) mounted read-only at `/Scores.txt` |

## Project stages
- [x] **Part 1** - Foundations: console application with three games
- [x] **Part 2** - Scores and containers: score file, Flask service, Docker, Selenium test
- [ ] **Part 3** - External storage, automation and deployment

