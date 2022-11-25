import pandas as pd
from network import Network
from data.dataset import LoadData
from model.model_cosine_similarity import SongRecommender

class TrackNetwork(Network):

    def __init__(self, limit=10, artistrelated=5, artisttracks=3, src="1k"):
        # self.track_info = track_info
        self.limit = limit
        self.artistrelated = artistrelated
        self.artisttracks = artisttracks
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