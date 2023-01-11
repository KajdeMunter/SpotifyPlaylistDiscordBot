# SpotifyPlaylistDiscordBot
A bot for discord that sends a message every time someone adds a song to a playlist. Includes a Makefile to get set up 
locally or build and publish to Docker Hub.

## instructions:
* Install [Docker](https://docs.docker.com/install/)
* Install [Docker Compose](https://docs.docker.com/compose/)
* Add correct environment variables to the docker-compose.yml
* Run `docker-compose up -d`

## Environment variables:
Please go through the [Spotify documentation](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)
to get your client id and secret. Use the [Discord docs](https://discordapp.com/developers/applications) to retrieve your token.
