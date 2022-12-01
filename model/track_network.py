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