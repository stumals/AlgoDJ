import pandas as pd


class LoadData():
    
    def __init__(self, src="million"):
        if src == "million":
            self.df_raw = pd.read_csv('./data/tracks_features.csv')
        else:
            self.df_raw = pd.read_csv('./data/music_data_1k.csv')
        self.df_raw['artists'] = self.df_raw.loc[:,'artists'].str.strip("[]'").str.split(',')
    
    def get_data(self) -> pd.DataFrame:
        return self.df_raw