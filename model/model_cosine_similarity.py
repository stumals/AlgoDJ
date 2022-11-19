import pandas as pd
import numpy as np
import networkx as nx
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
pd.options.mode.chained_assignment = None
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

df_raw = pd.read_csv('tracks_features.csv')
df_raw['artists'] = df_raw.loc[:,'artists'].str.strip("[]'").str.split(',')

class SongRecommender():
    
    def __init__(self, df_raw, song_name, song_id=None, client_id=None, client_secret=None):

        assert song_name in list(df_raw['name']), 'Song not in tracks_features dataset'
            
        if song_id == None:
            self.song_info = df_raw[df_raw['name']==song_name].iloc[0,:]
        else:
            self.song_info = df_raw[df_raw['id']==song_id]
            
        self.df_raw = df_raw
        
    def cosine_sim_calc(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        '''
        Calculate cosine similarity for all songs
        x: numpy array of attributes of each song from dataset
        y: numpy array of attributes of song that is being compared to dataset
        Returns numpy array with similarity score for each song in dataset
        '''
        dot_prods = (x*y).sum(1)
        x_norm = np.linalg.norm(x, axis=1)
        y_norm = np.linalg.norm(y, axis=1)
        norm_prod = x_norm * y_norm
        
        return dot_prods/norm_prod

    def recommender(self, num_songs=10):
        
        songs = self.df_raw.copy()
        keep_cols = ['danceability', 'energy', 'acousticness', 'valence', 'tempo',
                    'loudness', 'key', 'mode', 'speechiness', 'instrumentalness',
                    'time_signature', 'liveness']
        df = self.df_raw[keep_cols]
        song_index = self.df_raw[self.df_raw['id'].eq(self.song_info['id'])].index[0]

        x = df.to_numpy()
        y = x[song_index,:].reshape(1,-1).repeat(x.shape[0], axis=0)

        cosine_sim = self.cosine_sim_calc(x, y)
        songs['similarity_score'] = cosine_sim

        sorted_ids = np.argsort(cosine_sim)[::-1][:num_songs]

        #return songs.sort_values(by='similarity_score', ascending=False).iloc[:num_songs, :]
        return songs.loc[sorted_ids, :]

def artist_network(df_raw, playlist, limit=20, num_songs=10, num_related=5):
    '''
    Build artist network based artist of first song in playlist

    limit: number of times to generate of playlist from arists being generated in network
    num_songs: number of songs generated from each additional playlist
    num_related: number of additional artists to add to network

    returns networkx graph
    '''

    graph = nx.Graph()
    artists_base = list(playlist['artists'])
    song_ids_base = list(playlist['id'])
    song_names_base = list(playlist['name'])
    artist_main = artists_base[0][0]
    for artist_list in artists_base:
        for a in artist_list:
            graph.add_node(a)
            graph.add_edge(artist_main, a)
    i = 1
    while i < limit:
        new_playlist = SongRecommender(df_raw, song_names_base[i], song_id=song_ids_base[i]).recommender(num_songs=num_songs)
        artists_new = list(new_playlist['artists'])
        song_ids_new = list(new_playlist['id'])
        song_names_new = list(new_playlist['name'])

        artist_main = artists_new[0][0]
        for artist_list in artists_new:
            for a in artist_list:
                graph.add_node(a)
                graph.add_edge(artist_main, a)

        for j in range(num_related):
            song_ids_base.append(song_ids_new[j])
            song_names_base.append(song_names_new[j])
        i += 1
        
    graph.remove_edges_from(nx.selfloop_edges(graph))

    return graph
