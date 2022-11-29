import pdb
import networkx as nx
from data.dataset import LoadData
from model.model_cosine_similarity import SongRecommender

class Network():
    
    # set defaults for class variables  
    limit = 10
    num_songs = 5
    num_related = 3
    
    def __init__(self, limit, num_songs, num_related):
        self.limit = limit
        self.num_songs = num_songs
        self.num_related = num_related
        self.songbank = LoadData("1k").get_data()
        
    
    def build_network(self, df_raw, playlist, type) -> nx.Graph:
        '''
        Build artist network based on artist of first song in playlist

        limit: number of times to generate of pipplaylist from arists being generated in network
        num_songs: number of songs generated from each additional playlist
        num_related: number of additional artists to add to network

        returns networkx graph
        '''

        def _get_main_metric(type, artists_base, song_ids_base, song_names_base) -> tuple:
            
            # flatten the artist list
            artists_base = [num for elem in artists_base for num in elem]
            
            if type == "track":
                main_metric = (song_ids_base[0], song_names_base[0])
                main_metric_list = list(zip(song_ids_base, song_names_base))
            else:
                main_metric = artists_base[0]
                main_metric_list = artists_base
            return (main_metric, main_metric_list)
        
        def _update_graph(graph, main_metric, main_metric_list) -> None:
            for m in main_metric_list:
                graph.add_node(m)
                graph.add_edge(main_metric, m)
                
        def _append_songs(song_ids_base, song_names_base) -> None:
            for j in range(self.num_related):
                song_ids_base.append(song_ids_new[j])
                song_names_base.append(song_names_new[j])
        
        graph = nx.Graph()
        pdb.set_trace()
        artists_base = list(playlist['artists'])
        song_ids_base = list(playlist['id'])
        song_names_base = list(playlist['name'])
        
        main_metric, main_metric_list = _get_main_metric(type, artists_base, song_ids_base, song_names_base)
        
        _update_graph(graph, main_metric, main_metric_list)
                
        i = 1
        while i < self.limit:
            new_playlist = SongRecommender(df_raw, song_names_base[i], song_id=song_ids_base[i]).recommender(num_songs=self.num_songs)
            artists_new = list(new_playlist['artists'])
            song_ids_new = list(new_playlist['id'])
            song_names_new = list(new_playlist['name'])

            main_metric, main_metric_list = _get_main_metric(type, artists_new, song_ids_new, song_names_new)
        
            _update_graph(graph, main_metric, main_metric_list)

            _append_songs(song_ids_base, song_names_base)

            i += 1
            
        graph.remove_edges_from(nx.selfloop_edges(graph))

        return graph