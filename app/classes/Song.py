"""app folder: Song class
"""

 
 
class Song(object):
    def __init__(self, song_dict):
        for k in song_dict:
            setattr(self, k, song_dict[k])
            
            
            


# test

if __name__ == '__main__':
    song1_dict = {"title":"Anti-Hero", "artist":"Taylor Swift", "album":"Midnights (3am Edition)", "genre":"Pop"}
    
    song2_dict = {"title":"", "artist":"", "genre": "", "year":"", "beats per minute":"","energy":"", "danceability":"", "loudness":"", "liveness":"", "valence":"", "length":"", "acousticness":"", "speechiness":"", "popularity":""}
    
    song1=Song(song1_dict)
    
    print(song1.artist)

        
        