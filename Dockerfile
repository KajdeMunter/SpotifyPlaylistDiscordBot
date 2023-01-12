FROM --platform=linux/amd64 python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["python3", "-u", "SpotifyDiscordBot.py"]
