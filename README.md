# SpotifyPlaylistDiscordBot
A bot for discord that sends a message every time someone adds a song to a playlist.

## instructions: ##
* install [discord.py](https://github.com/Rapptz/discord.py)
* install [spotipy](https://github.com/plamere/spotipy)
* fill in the strings for `SpotifyClient('client_id', 'client_secret', 'playlist_uri')`
* fill in channel_id `await discordclient.send_message(discord.Object(id='channel_id'), output)`
* fill in the discord bot token `discordclient.run('discord_token')`
* run SpotifyDiscordBot.py!
