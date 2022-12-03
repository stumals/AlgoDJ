
import pandas as pd
import numpy as np
import networkx as nx
import datetime
pd.options.mode.chained_assignment = None
import warnings
from typing import Tuple
warnings.filterwarnings("ignore")

class SongRecommenderCached():
    def __init__(self, songsample):
        self.songsample = songsample

class SongRecommender():
    
    def __init__(self, df_raw, song_name, song_id=None, gender='NA', age='NA', decade_range=1.5):

        assert song_name in list(df_raw['name']), 'Song not in tracks_features dataset'
        
        self.song_name = song_name
        self.song_id = song_id
        self.gender = gender
        self.age = age
        self.decade_range = decade_range

        if self.song_id == None:
            self.song_info = df_raw[df_raw['name']==song_name].iloc[0,:]
        else:
            # song id used used when building artist network (some songs have same name)
            self.song_info = df_raw[df_raw['id']==song_id]
            # set age to 'NA' when building artist network
            self.age = 'NA'

        if self.age == 'NA':
            self.df_raw = df_raw
        else:
            year = datetime.datetime.now().year
            year_born = year - self.age
            year_var = self.decade_range * 10
            self.df_raw = df_raw[(df_raw['year'] <= (year_born + year_var)) & (df_raw['year'] >= (year_born - year_var))]

            # add selected song back to dataset in case it was filtered out by year
            row = self.song_info.to_frame().transpose()
            if self.df_raw[self.df_raw['id'].eq(row['id'])].empty:
                self.df_raw = pd.concat([row, self.df_raw], axis=0)
            # reset indices of dataframe
            self.df_raw = self.df_raw.reset_index(drop=True)
        
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

    def recommender(self, num_songs=10) -> Tuple[pd.DataFrame, ...]:
        '''
        Top num_songs recommended based on cosine similarity score using keep_cosl
        Keep cols are determined by self.gender
        
        Returns pandas dataframe of recommendations and self.df_raw that was filtered based on age input (to be used in artist_network)
        '''
        
        songs = self.df_raw.copy()
        if self.gender == 'NA':
            keep_cols = ['danceability', 'energy', 'acousticness', 'valence', 'tempo',
                        'loudness', 'key', 'mode', 'speechiness', 'instrumentalness',
                        'time_signature', 'liveness']
        elif self.gender.lower() == 'male':
            keep_cols = ['energy', 'acousticness', 'valence', 'tempo',
                        'loudness', 'key', 'mode', 'instrumentalness',
                        'liveness']
        else:
            keep_cols = ['danceability', 'energy', 'acousticness', 'valence',
                        'loudness', 'key', 'mode', 'speechiness', 'time_signature']
                
        df = self.df_raw[keep_cols]
        song_index = self.df_raw[self.df_raw['id'].eq(self.song_info['id'])].index[0]

        x = df.to_numpy().astype(float)
        y = x[song_index,:].reshape(1,-1).repeat(x.shape[0], axis=0).astype(float)

        cosine_sim = self.cosine_sim_calc(x, y)
        songs['similarity_score'] = cosine_sim

        sorted_ids = np.argsort(cosine_sim)[::-1][:num_songs]

        return (songs.loc[sorted_ids, :], songs)
