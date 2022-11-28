import pandas as pd
from pathlib import Path


class LoadData():
    
    def __init__(self, src="million"):
        if src == "million":
            # self.df_raw = pd.read_csv(Path(Path.cwd(), 'data', 'tracks_features.csv'))
            self.df_raw = pd.read_csv('s3://algodjdatabucket/tracks_features.csv', storage_options={"anon": True})
        else:
            self.df_raw = pd.read_csv(Path(Path.cwd(), 'data', 'music_data_1k.csv'))
        self.df_raw['artists'] = self.df_raw.loc[:,'artists'].str.strip("[]'").str.split(',')
        
        # 10 rows have 0 for year and release date for same album
        self.df_raw[self.df_raw['year']==0] = 2018
        self.df_raw['year'] = self.df_raw['year'].astype(int)

        self.df_raw[self.df_raw['release_date']=='0000'] = '2018-09-04'
        self.df_raw['release_date'] = pd.to_datetime(self.df_raw['release_date'])

        value_cols = ['danceability', 'energy', 'acousticness', 'valence', 'tempo',
                        'loudness', 'key', 'mode', 'speechiness', 'instrumentalness',
                        'time_signature', 'liveness']
        self.df_raw[value_cols] = self.df_raw[value_cols].astype(float)

    
    def get_data(self) -> pd.DataFrame:
        return self.df_raw 