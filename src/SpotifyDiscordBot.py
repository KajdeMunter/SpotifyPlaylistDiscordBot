import discord
import asyncio
import SpotifyClient
import os
import pandas as pd

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
spotifyclient = SpotifyClient.SpotifyClient(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'], os.environ['PLAYLIST_URI'])

# Create an instance of Watcher with the initial "old" value parameter
watcher = Watcher(spotifyclient.get_playlist_tracks(spotifyclient.username, spotifyclient.playlist_id))

# instantiate the discord client
discordclient = discord.Client()

@discordclient.event
async def on_ready():
    print('Logged in as')
    print(discordclient.user.name)
    print(discordclient.user.id)
    print('------')
    print('Checking for newly added songs...')

    while True:
        await asyncio.sleep(SpotifyClient.Checkevery)
        # runs the set_value method of watcher to see if the playlist has changed from its original state
        playlistTracks = watcher.set_value(spotifyclient.get_playlist_tracks(spotifyclient.username, spotifyclient.playlist_id))

        # discord throws an exception if the message is empty (this happens when there is no new song and so the spotify client returns nothing)
        if playlistTracks is not None:
            for track in range(len(playlistTracks)):
                # Format the output
                output = playlistTracks[track]['added_by']['id'] + ' added a song: "' + playlistTracks[track]['track']['name'] + '" by "' + playlistTracks[track]['track']['artists'][0]['name'] + '"!'
                # Save the output
                SpotifyClient.SpotifyClient.set_last_song_sent_to_DC(playlistTracks[track]['added_at'])
                # Print to discord channel
                await discordclient.get_channel(int(os.environ['CHANNEL_ID'])).send(output)

@discordclient.event
async def on_message(message):
    if message.author == discordclient.user:
        return

    if message.content.lower() == 'f':
        await message.channel.send('Lekker voor je')

    if message.content.lower() == 'stats':
        tracks = spotifyclient.get_playlist_tracks(spotifyclient.username, spotifyclient.playlist_id)

        output = {}
        for track in tracks:
            user = track['added_by']['id']
            if user in output:
                output[user] +=1
            else:
                output[user] =1

        for k, v in dict(sorted(output.items(), reverse=True, key=lambda item: item[1])).items():
            await message.channel.send(k + ': ' + str(v))

# finally, run the discord client
discordclient.run(os.environ['DISCORD_TOKEN'])
