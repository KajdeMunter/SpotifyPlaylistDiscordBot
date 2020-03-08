FROM alpine:3.11 AS build

WORKDIR /opt/app

ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

COPY Pipfile Pipfile.lock /opt/app/

RUN apk add --no-cache \
      python3 \
      python3-dev \
      py3-pip \
      libffi \
      libffi-dev \
      musl-dev \
      gcc \
 && pip3 install pipenv \
 && python3 -m venv /opt/venv \
 && pipenv install --deploy

FROM alpine:3.11

ENV PATH="/opt/venv/bin:$PATH" VIRTUAL_ENV="/opt/venv"

WORKDIR /opt/app

RUN apk add --no-cache \
      python3 \
      libffi \
 && addgroup -g 1000 rungroup \
 && adduser -u 1000 -S -G rungroup runuser

COPY --from=build --chown=runuser:rungroup /opt/venv /opt/venv
COPY --chown=runuser:rungroup ./src /opt/app/

USER runuser:rungroup

ENTRYPOINT ["python", "SpotifyDiscordBot.py"]
