import pandas as pd
import pickle
import os
from pathlib import Path


def create_pickle_data(track_network_obj, song_name, num_songs_playlist):

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
    network_artist = track_network_obj.build_network(recs, 'artist')
    network_track = track_network_obj.build_network(recs, 'track')
    playlist = track_network_obj.get_playlist(recs, num_songs=num_songs_playlist)

    # create pickle files
    playlist.to_pickle("{}_playlist.pickle".format(song_name))
    with open('{}_network_{}.pickle'.format(song_name, 'artist'), 'wb') as f:
        pickle.dump(network_artist, f)
    with open('{}_network_{}.pickle'.format(song_name, 'track'), 'wb') as f:
        pickle.dump(network_track, f) 


def get_pickle_data(song_name: str) -> dict:

    # Assumes current working directory is AlgoDJ project
    dirpath = Path(Path.cwd(), "data", "pickle_data", song_name)
    data = {}
    data['playlist'] = pd.read_pickle(Path(dirpath, '{}_playlist.pickle'.format(song_name)))
    
    with open(Path(dirpath, '{}_network_artist.pickle'.format(song_name)), 'rb') as f:
        data['network_artist'] = pickle.load(f)

    with open(Path(dirpath, '{}_network_track.pickle'.format(song_name)), 'rb') as f:
        data['network_track'] = pickle.load(f)
    
    return data

