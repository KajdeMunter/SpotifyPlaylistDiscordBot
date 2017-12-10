import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime, timedelta

# The amount of seconds the bot should call the API to see if there are songs added
Checkevery = 300

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

    @staticmethod
    def get_last_added(tracks):
        # Spotify added_at returns YYYY-MM-DDTHH:MM:SSZ in UTC.
        new_songlist = []
        for i in range(len(tracks)):
            if datetime.strptime(tracks[i]['added_at'], '%Y-%m-%dT%H:%M:%SZ') > datetime.utcnow() - timedelta(seconds=Checkevery):
                new_songlist.append(tracks[i])
        return new_songlist
