import networkx as nx
from typing import List, Tuple
from spotipyauth import SpotipyAuth

class ArtistNetwork(SpotipyAuth):
    
    sp = SpotipyAuth.client

    def __init__(self, artist, limit=100, num_related=5):
        self.artist = artist
        self.limit = limit
        self.num_related = num_related
        self.artist_data = self.sp.search(q=self.artist, type='artist')
        self.artist_id = self.artist_data['artists']['items'][0]['id']
        self.artist_name = self.artist_data['artists']['items'][0]['name']
        self.artist_info = (self.artist_id, self.artist_name)

    def get_related_artists(self, artist_id: str = None) -> List[Tuple]:
        if artist_id is None:
            artist_id = self.artist_id
        related = []
        r = self.sp.artist_related_artists(artist_id)
        for a in r['artists']:
            related.append((a['id'], a['name']))
        return related[:self.num_related]

    def create_artist_network(self) -> None:
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

    def create_graph(self) -> None:
        self.g = nx.Graph()
        for n in self.nodes:
            self.g.add_node(n)
        for e in self.edges:
            self.g.add_edge(e[0], e[1])
    
    def sort_graph_pagerank(self) -> None:
        pagerank = nx.pagerank(self.g)
        pagerank_sorted = sorted(pagerank.items(), key=lambda x:x[1], reverse=True)
        self.g = pagerank_sorted