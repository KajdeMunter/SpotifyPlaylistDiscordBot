# SpotifyPlaylistDiscordBot
A bot for discord that sends a message every time someone adds a song to a playlist. Includes a Makefile to get set up 
locally or build and publish to Docker Hub.

## instructions:
* Install [Docker](https://docs.docker.com/install/)
* `docker pull kajdemunter/spotifyplaylistdiscordbot:latest`
* Run the image with correct environment variables:

```
docker run -d \
    -e CLIENT_ID=<value> \
    -e CLIENT_SECRET=<value> \
    -e PLAYLIST_URI=<value> \
    -e CHANNEL_ID=<value> \
    -e DISCORD_TOKEN=<value> \
    kajdemunter/spotifyplaylistdiscordbot:latest
```

## Environment variables:
CLIENT_ID
CLIENT_SECRET
PLAYLIST_URI
CHANNEL_ID
DISCORD_TOKEN
