from flask import Flask, render_template

from Score import read_score
from Utils import BAD_RETURN_CODE

# Internal port of the score service. Docker maps host port 8777 to it.
PORT = 5000

app = Flask(__name__)


@app.route("/", methods=["GET"])
def score_server():
    score = read_score(missing_is_zero=False)
    if score == BAD_RETURN_CODE:
        return render_template("score.html", error="Error: the score is not available."), 500
    return render_template("score.html", score=score)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

