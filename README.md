# World of Games (WoG)

A Python console application with three playable games, built as a cumulative DevOps course project.

## Games
1. **Memory Game** - a sequence of numbers appears for 0.7 seconds; repeat it in the same order.
2. **Guess Game** - guess the secret number the computer picked.
3. **Currency Roulette** - estimate the ILS value of a random USD amount, using a live exchange rate.

Difficulty ranges from 1 (easiest) to 5 (hardest).

## Requirements
- Python 3.10+
- Internet connection (for Currency Roulette)

## How to run
```bash
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
python MainGame.py

```

## Project structure
| File | Purpose |
|---|---|
| `MainGame.py` | Entry point |
| `Live.py` | Welcome message, main menu, game selection and input validation |
| `GuessGame.py` | Guess Game logic |
| `MemoryGame.py` | Memory Game logic |
| `CurrencyRouletteGame.py` | Currency Roulette logic and exchange-rate API |
| `requirements.txt` | External Python dependencies |

## Project stages
- [x] **Part 1** - Foundations: console application with three games
- [ ] **Part 2** - Scores and web service
- [ ] **Part 3** - Containers, automation and deployment

