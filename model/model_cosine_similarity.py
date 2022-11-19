#%%
import pandas as pd
import numpy as np
import networkx as nx
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
pd.options.mode.chained_assignment = None

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
#%%
df_raw = pd.read_csv('tracks_features.csv')
df_raw['artists'] = df_raw.loc[:,'artists'].str.strip("[]'").str.split(',')
#%%
class SongRecommender():
    
    def __init__(self, df_raw, song_name, client_id=None, client_secret=None):

        self.song_info = df_raw[df_raw['name']==song_name].iloc[0,:]
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

        # returns dataframe with song name, artists, and similarity score
        return songs.sort_values(by='similarity_score', ascending=False).iloc[:num_songs, :]    
#%%
