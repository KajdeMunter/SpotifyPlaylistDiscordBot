SHELL := /bin/bash

MAKEFLAGS := --silent --no-print-directory

.DEFAULT_GOAL := help

.PHONY: help up

export secrets_dir :=$(CURDIR)/../.devnl-backend-vault/

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9\._-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

publish: ## Build and publish to docker hub. Args: tag
	docker build . -t kajdemunter/spotifyplaylistdiscordbot:$(tag)
	docker push kajdemunter/spotifyplaylistdiscordbot:$(tag)

run: ## Build and run container locally using exported environment variables
	docker build . -t spotifyplaylistdiscordbot
	docker run -d \
		-e CLIENT_ID \
		-e CLIENT_SECRET \
		-e PLAYLIST_URI \
		-e CHANNEL_ID \
		-e DISCORD_TOKEN \
		spotifyplaylistdiscordbot:latest
