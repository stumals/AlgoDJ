import pandas as pd
from pathlib import Path


class LoadData():
    
    def __init__(self, src="million"):
        if src == "million":
            self.df_raw = pd.read_csv(Path(Path.cwd(), 'data', 'tracks_features.csv'))
            # self.df_raw = pd.read_csv('s3://algodjdatabucket/tracks_features.csv', storage_options={"anon": True})
        else:
            self.df_raw = pd.read_csv(Path(Path.cwd(), 'data', 'music_data_1k.csv'))
        self.df_raw['artists'] = self.df_raw.loc[:,'artists'].str.strip("[]'").str.split(',')
    
    def get_data(self) -> pd.DataFrame:
        return self.df_raw 