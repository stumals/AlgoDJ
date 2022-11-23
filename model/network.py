import networkx as nx
from model.model_cosine_similarity import SongRecommender

class Network():
    
    # set defaults for class variables
    # limit = 20
    # num_songs = 10
    # num_related = 5
    
    limit = 10
    num_songs = 5
    num_related = 3
    
    def __init__(self, limit, num_songs, num_related):
        self.limit = limit
        self.num_songs = num_songs
        self.num_related = num_related
        
    
    def build_network(self, df_raw, playlist, type) -> nx.Graph:
        '''
        Build artist network based artist of first song in playlist

        limit: number of times to generate of pipplaylist from arists being generated in network
        num_songs: number of songs generated from each additional playlist
        num_related: number of additional artists to add to network

        returns networkx graph
        '''

        def _get_main_metric(type, artists_base, song_names_base):
            if type == "track":
                main_metric = song_names_base[0][0]
                main_metric_list = song_names_base
            else:
                main_metric = artists_base[0][0]
                main_metric_list = artists_base
            return (main_metric, main_metric_list)
        
        graph = nx.Graph()
        artists_base = list(playlist['artists'])
        song_ids_base = list(playlist['id'])
        song_names_base = list(playlist['name'])
        
        main_metric, main_metric_list = _get_main_metric(type, artists_base, song_names_base)
        
        for ml in main_metric_list:
            for m in ml:
                graph.add_node(m)
                graph.add_edge(main_metric, m)
                
        i = 1
        while i < self.limit:
            new_playlist = SongRecommender(df_raw, song_names_base[i], song_id=song_ids_base[i]).recommender(num_songs=self.num_songs)
            artists_new = list(new_playlist['artists'])
            song_ids_new = list(new_playlist['id'])
            song_names_new = list(new_playlist['name'])

            main_metric, main_metric_list = _get_main_metric(type, artists_new, song_names_new)
        
            for ml in main_metric_list:
                for m in ml:
                    graph.add_node(m)
                    graph.add_edge(main_metric, m)

            for j in range(self.num_related):
                song_ids_base.append(song_ids_new[j])
                song_names_base.append(song_names_new[j])
            i += 1
            
        graph.remove_edges_from(nx.selfloop_edges(graph))

        return graph