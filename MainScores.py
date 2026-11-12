from flask import Flask

from Score import read_score
from Utils import BAD_RETURN_CODE

# Internal port of the score service. Docker maps host port 8777 to it.
PORT = 5000

SCORE_PAGE = """<!DOCTYPE html>
<html>
<head><title>Scores Game</title></head>
<body>
<h1>The score is <span id="score">{score}</span></h1>
</body>
</html>"""

ERROR_PAGE = """<!DOCTYPE html>
<html>
<head><title>Scores Game</title></head>
<body>
<h1><span id="score" style="color: red">{error}</span></h1>
</body>
</html>"""

app = Flask(__name__)


@app.route("/", methods=["GET"])
def score_server():
    score = read_score(missing_is_zero=False)
    if score == BAD_RETURN_CODE:
        return ERROR_PAGE.format(error="Error: the score is not available."), 500
    return SCORE_PAGE.format(score=score)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

