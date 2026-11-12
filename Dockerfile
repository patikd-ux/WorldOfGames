# Score service of World of Games (Flask)
FROM python:3.14-slim

WORKDIR /app

# Install dependencies first, so this layer is cached when only the code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only the files the score service needs
COPY Utils.py Score.py MainScores.py ./
COPY templates/ templates/

# Part 2: an initial score file inside the image (Part 3 moves it to external storage)
RUN echo 0 > /Scores.txt
ENV WOG_SCORES_FILE=/Scores.txt

# Internal port of the service (PORT in MainScores.py); mapped to 8777 on the host
EXPOSE 5000

CMD ["python", "MainScores.py"]

