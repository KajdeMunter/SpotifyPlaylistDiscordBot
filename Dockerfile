FROM --platform=linux/amd64 python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src .

CMD ["python3", "SpotifyDiscordBot.py"]
