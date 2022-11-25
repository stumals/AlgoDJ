import pandas as pd
from model.network import Network
from data.dataset import LoadData
from model.model_cosine_similarity import SongRecommender

class TrackNetwork(Network):

    def __init__(self, limit=27, num_songs=3, num_related=3, src="1k"):
        # self.track_info = track_info
        self.limit = limit
        self.num_songs = num_songs
        self.num_related = num_related
        self.src = src
        self.songbank = LoadData(self.src).get_data()

    def get_playlist(self, songsample) -> pd.DataFrame:
        return SongRecommender(self.songbank, songsample).recommender()
    
    
    
if __name__ == "__main__":
    track_network = TrackNetwork()
    playlist = track_network.get_playlist("Saints Go Marching In")
    network = track_network.build_network(track_network.songbank, playlist, "artist")
    print(network.nodes())
    # print(sp_obj.get_related_tracks(sp_obj.get_related_artists(sp_obj.artist_id)))