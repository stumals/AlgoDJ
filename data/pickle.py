import pandas as pd
import pickle
import os
from pathlib import Path
from typing import List
from model.track_network import TrackNetwork


def create_pickle_data(track_network_obj, song_name, network_type, num_songs_playlist):

    # Assumes current working directory is AlgoDJ project
    assert os.getcwd()[-6:] == 'AlgoDJ', 'Current directory not in AlgoDJ project'    
    os.chdir(Path.cwd() / 'data' / 'pickle_data')

    # check if song_name is a folder in pickle_data or not
    try:
        os.chdir(Path.cwd() / song_name)
    except:
        os.mkdir(Path.cwd() / song_name)
        os.chdir(Path.cwd() / song_name)
    
    # create data with track_network object, network type, song name
    recs = track_network_obj.get_recommendations(song_name)
    network = track_network_obj.build_network(recs, network_type)
    playlist = track_network_obj.get_playlist(recs, num_songs=num_songs_playlist)

    # create pickle files
    playlist.to_pickle("{}_playlist.pickle".format(song_name))
    with open('{}_network_{}.pickle'.format(song_name, network_type), 'wb') as f:
        pickle.dump(network, f) 


def get_pickle_data():
    pass