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

    # @staticmethod
    # def get_song_info(song_name, client_id, client_secret):
    #     '''
    #     Get song info and features from spotify api based on song_name
    #     '''
    #     sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
    #     song_data = sp.search(q=song_name, type='track')
    #     song_info = {}
    #     song_info['id'] = song_data['tracks']['items'][0]['id']
    #     song_info['name'] = song_data['tracks']['items'][0]['name']
    #     song_info['artists'] = song_data['tracks']['items'][0]['artists'][0]['name']
    #     song_info['album'] = song_data['tracks']['items'][0]['album']['name']
        
    #     features = sp.audio_features(song_info['id'])[0]
    #     song_info['danceability'] = features['danceability']
    #     song_info['energy'] = features['energy']
    #     song_info['acousticness'] = features['acousticness']
    #     song_info['valence'] = features['valence']
    #     song_info['tempo'] = features['tempo']
    #     song_info['loudness'] = features['loudness']
    #     song_info['key'] = features['key']
    #     song_info['mode'] = features['mode']
    #     song_info['speechiness'] = features['speechiness']
    #     song_info['instrumentalness'] = features['instrumentalness']
    #     song_info['time_signature'] = features['time_signature']
    #     song_info['liveness'] = features['liveness']
        
    #     return song_info
    
    def __init__(self, df_raw, song_name, client_id=None, client_secret=None):

        # if song_name not in list(df_raw.loc[:,'name']):
        #     self.song_info = SongRecommender.get_song_info(song_name, client_id, client_secret)
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

        # using name and artist columns for output of recommender
        
        songs = self.df_raw.copy()
        keep_cols = ['danceability', 'energy', 'acousticness', 'valence', 'tempo',
                    'loudness', 'key', 'mode', 'speechiness', 'instrumentalness',
                    'time_signature', 'liveness']
        df = self.df_raw[keep_cols]
        
        # check to see if song from input is in the dataset or not. If not, add to data
        # if self.df_raw[self.df_raw['id'].eq(self.song_info['id'])].empty:  
        #     new_features = pd.DataFrame(self.song_info, index=[0]).loc[:,keep_cols]
        #     df = pd.concat([new_features, df.loc[:]]).reset_index(drop=True)
        #     new_song = pd.DataFrame(self.song_info, index=[0]).loc[:,['name', 'artists']]
        #     songs = pd.concat([new_song, songs]).reset_index(drop=True)
        #     song_index = 0
        # else:
        #     song_index = self.df_raw[self.df_raw['id'].eq(self.song_info['id'])].index[0]
        song_index = self.df_raw[self.df_raw['id'].eq(self.song_info['id'])].index[0]

        x = df.to_numpy()
        y = x[song_index,:].reshape(1,-1).repeat(x.shape[0], axis=0)

        cosine_sim = self.cosine_sim_calc(x, y)
        songs['similarity_score'] = cosine_sim

        # returns dataframe with song name, artists, and similarity score
        return songs.sort_values(by='similarity_score', ascending=False).iloc[:num_songs, :]

    def artist_network(self, limit=100, num_related=3):


#%%
client_id = '6dcf8d2d2669452caf7d01db534e711f'
client_secret = '6054228a75434cd5bc34fa6e13900f7b'
#%%

playlist = SongRecommender(df_raw, 'She Belongs to Me')
p = playlist.recommender(num_songs=10)

# %%
SongRecommender(df_raw, p.iloc[1,1]).recommender(num_songs=10)
# %%
p
# %%
