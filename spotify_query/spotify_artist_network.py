import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import networkx as nx

class ArtistNetwork():

    def __init__(self, artist, client_id, client_secret, limit=100, num_related=5):
        self.artist = artist
        self.limit = limit
        self.num_related = num_related
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

        artist_data = self.sp.search(q=self.artist, type='artist')
        artist_id = artist_data['artists']['items'][0]['id']
        artist_name = artist_data['artists']['items'][0]['name']
        self.artist_info = (artist_id, artist_name)

    def get_related_artists(self, artist_id):
        related = []
        r = self.sp.artist_related_artists(artist_id)
        for a in r['artists']:
            related.append((a['id'], a['name']))
        return related[:self.num_related]

    def get_artist_network(self):
        artist_id = self.artist_info[0]
        ids = []
        ids.append(artist_id)
        network = []
        r = self.get_related_artists(artist_id)
        for a in r:
            ids.append(a)
            network.append((self.artist_info[1], a[1]))
        i = 1
        while i < self.limit:
            r = self.get_related_artists(ids[i][0])
            for a in r:
                network.append((ids[i][1], a[1]))
                if a not in ids:
                    ids.append(a)
            i += 1
        self.nodes = []
        for name in ids:
            self.nodes.append(name[1])
        self.edges = network[:]

    def create_graph(self):
        self.g = nx.Graph()
        for n in self.nodes:
            self.g.add_node(n)
        for e in self.edges:
            self.g.add_edge(e[0], e[1])
    
    def pagerank(self):
        pagerank = nx.pagerank(self.g)
        pagerank_sorted = sorted(pagerank.items(), key=lambda x:x[1], reverse=True)
        return pagerank_sorted
