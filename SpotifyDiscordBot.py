import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio


class Watcher:
    """ Watches is the value of the variable changes and runs post_change method if it is """
    def __init__(self, value):
        self.value = value

    def set_value(self, new_value):
        if self.value != new_value:
            self.value = new_value
            return self.post_change()

    # returns a formatted version of the json object from the spotify api
    def post_change(self):
        return self.value[-1]['added_by']['id'] + ' just added a song: "' + self.value[-1]['track']['name'] + '" by "' + self.value[-1]['track']['artists'][0]['name'] + '"!'


class SpotifyClient:
    def __init__(self, client_id, client_secret, uri):
        self.client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        self.uri = uri
        self.username = uri.split(':')[2]
        self.playlist_id = uri.split(':')[4]
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    # The standard spotify playlist reader has a max of 100 songs so we have to loop and append through the entire playlist
    def get_playlist_tracks(self, username, playlist_id):
        results = self.sp.user_playlist_tracks(username, playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks

# Create an instance of spotifyclient with client_id, client_secret and the spotify playlist uri
spotifyclient = SpotifyClient('', '', '')

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
    # loops every 5 minutes
    while True:
        await asyncio.sleep(300)
        # runs the set_value method of watcher to see if the playlist has changed from its original state
        output = watcher.set_value(spotifyclient.get_playlist_tracks(spotifyclient.username, spotifyclient.playlist_id))

        # discord throws an exception if the message is empty (this happens when there is no new song and so the spotify client returns nothing)
        if output is not None:
            await discordclient.send_message(discord.Object(id=''), output)

# finally, run the discord client
discordclient.run('')
