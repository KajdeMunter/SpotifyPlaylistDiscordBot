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
            if datetime.strptime(tracks[i]['added_at'], '%Y-%m-%dT%H:%M:%SZ') > datetime.utcnow() - timedelta(seconds=Checkevery) or datetime.strptime(tracks[i]['added_at'], '%Y-%m-%dT%H:%M:%SZ') > SpotifyClient.get_last_song_sent_to_DC():
                new_songlist.append(tracks[i])
        return new_songlist

    @staticmethod
    def get_last_song_sent_to_DC():
        file_object = open("LastSongSentToDC.txt", "r")

        file_object.seek(0)
        first_char = file_object.read(1)
        if not first_char:
            # File is empty
            set_last_song_sent_to_DC(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        else:
            # First character wasn't empty, return to start of file.
            file_object.seek(0)

        return datetime.strptime(file_object.read(), '%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def set_last_song_sent_to_DC(text):
        file_object = open("LastSongSentToDC.txt", "w")
        file_object.write(text)
        file_object.truncate()
        file_object.close()

