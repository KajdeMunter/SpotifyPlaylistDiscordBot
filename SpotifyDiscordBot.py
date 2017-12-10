import discord
import asyncio
import SpotifyClient

# The amount of seconds the bot should call the API to see if there are songs added
Checkevery = 300


class Watcher:
    """ Watches is the value of the variable changes and runs post_change method if it is """
    def __init__(self, value):
        self.value = value

    def set_value(self, new_value):
        if self.value != new_value:
            self.value = new_value
            return self.post_change()

    # Returns a list of the songs added since last check
    def post_change(self):
        # return SpotifyClient.SpotifyClient.get_last_added(self.value)
        return SpotifyClient.SpotifyClient.get_last_added(self.value)

# Create an instance of spotifyclient with client_id, client_secret and the spotify playlist uri
spotifyclient = SpotifyClient.SpotifyClient('', '', '')

# Create an instance of Watcher with the initial "old" value parameter
watcher = Watcher(spotifyclient.get_playlist_tracks(spotifyclient.username, spotifyclient.playlist_id))

# instanciate the discord client
discordclient = discord.Client()


@discordclient.event
async def on_ready():
    print('Logged in as')
    print(discordclient.user.name)
    print(discordclient.user.id)
    print('------')
    print('Checking for newly added songs...')

    while True:
        await asyncio.sleep(Checkevery)
        # runs the set_value method of watcher to see if the playlist has changed from its original state
        playlistTracks = watcher.set_value(spotifyclient.get_playlist_tracks(spotifyclient.username, spotifyclient.playlist_id))

        # discord throws an exception if the message is empty (this happens when there is no new song and so the spotify client returns nothing)
        if playlistTracks is not None:
            for track in range(len(playlistTracks)):
                output = playlistTracks[track]['added_by']['id'] + ' added a song: "' + playlistTracks[track]['track']['name'] + '" by "' + playlistTracks[track]['track']['artists'][0]['name'] + '"!'
                await discordclient.send_message(discord.Object(id=''), output)

# finally, run the discord client
discordclient.run('')
