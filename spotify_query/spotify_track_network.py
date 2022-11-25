from typing import List, Tuple
from spotipyauth import SpotipyAuth
# from networkgraph import Graph

class TrackNetwork(SpotipyAuth):
    
    sp = SpotipyAuth.client

    def __init__(self, track_info, limit=100, artistrelated=5, artisttracks=3):
        self.track_info = track_info
        self.limit = limit
        self.artistrelated = artistrelated
        self.artisttracks = artisttracks
        self.track_data = self.sp.search(track_info, type="track")
        self.track_artists = self.track_data["tracks"]["items"][0]["artists"]
        self.artist_id = [self.track_artists[i]["id"] for i in range(len(self.track_artists))]
        self.artist_name = [self.track_artists[i]["name"] for i in range(len(self.track_artists))]
        self.track_name = self.track_data["tracks"]["items"][0]["name"]
        self.track_id = self.track_data["tracks"]["items"][0]["id"]
        
    def get_related_artists(self, artist_id: str = None) -> List[Tuple]:
        if artist_id is None:
            artist_id = self.artist_id
        related = []
        r = self.sp.artist_related_artists(artist_id)
        for a in r['artists']:
            related.append((a['id'], a['name']))
        return related[:self.num_related]
    
    def get_related_tracks(self, artist_tuple: tuple) -> List[Tuple]:
        related = []
        for a, i in artist_tuple:
            related.append(self.sp.artist_top_tracks(i))
        return related[:self.artisttracks]       
    
if __name__ == "__main__":
    # sp = TrackNetwork("6bM4daGlfZHtKMQp8tEqVz")
    sp_obj = TrackNetwork("Ego Death Polyphia")
    # print(sp_obj.trackname)
    # print(dir(sp_obj.sp))
    print(sp_obj.get_related_tracks(sp_obj.get_related_artists(sp_obj.artist_id)))