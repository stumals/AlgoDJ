import pdb
import pandas as pd
import networkx as nx
from data.dataset import LoadData
from model.model_cosine_similarity import SongRecommender

class Network():
    
    # set defaults for class variables  
    limit = 10
    num_songs = 5
    num_related = 3
    src = "million"
    songbank = LoadData(src).get_data()
    
    def __init__(self, limit, num_songs, num_related):
        self.limit = limit
        self.num_songs = num_songs
        self.num_related = num_related
        
    @staticmethod
    def get_playlist(recommender_obj, num_songs=10) -> pd.DataFrame:
        # return only the filtered playlist
        return recommender_obj.recommender(num_songs)[0]
    
    def get_recommendations(self, songsample, song_id=None, gender='NA', age='NA', decade_range=1.5):
        return SongRecommender(self.songbank, songsample, song_id, gender, age, decade_range)
    
    def build_network(self, recommender_obj, type) -> nx.Graph:
        '''
        Build artist network based on artist of first song in playlist

        limit: number of times to generate of pipplaylist from arists being generated in network
        num_songs: number of songs generated from each additional playlist
        num_related: number of additional artists to add to network

        returns networkx graph
        '''

        def _get_main_metric(type, artists_base, song_ids_base, song_names_base) -> tuple:
            
            # flatten the artist list
            # pdb.set_trace()
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
        playlist = self.get_playlist(recommender_obj) 
        artists_base = list(playlist['artists'])
        song_ids_base = list(playlist['id'])
        song_names_base = list(playlist['name'])
        
        main_metric, main_metric_list = _get_main_metric(type, artists_base, song_ids_base, song_names_base)
        
        _update_graph(graph, main_metric, main_metric_list)
                
        i = 1
        while i < self.limit:
            # update recommender object with new song choice, but use old recommender object's metadata
            recommender_obj = SongRecommender(self.songbank, song_names_base[i], song_ids_base[i], 
                                            recommender_obj.gender, recommender_obj.age, recommender_obj.decade_range)
            new_playlist = self.get_playlist(recommender_obj)
            artists_new = list(new_playlist['artists'])
            song_ids_new = list(new_playlist['id'])
            song_names_new = list(new_playlist['name'])

            main_metric, main_metric_list = _get_main_metric(type, artists_new, song_ids_new, song_names_new)
        
            _update_graph(graph, main_metric, main_metric_list)

            _append_songs(song_ids_base, song_names_base)

            i += 1
            
        graph.remove_edges_from(nx.selfloop_edges(graph))

        return graph