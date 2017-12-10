import discord
import asyncio
import SpotifyClient


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

    # TODO check if there is songs added since the last saved song in LastSong.txt
    #   IF SONGS ADDED:
    #       SEND A MESSAGE TO DISCORD WITH WITH EVERY SONG THAT IS ADDED
    #       SAVE THE LAST ADDED SONG DATETIME
    #   IF NO SONGS ADDED:
    #       print('No new songs added!')

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
                await discordclient.send_message(discord.Object(id=''), output)

# finally, run the discord client
discordclient.run('')
