"""app folder: PlayList class
"""

 
 
class PlayList(object):
    def __init__(self, playList_dict):
        for k in playList_dict:
            setattr(self, k, playList_dict[k])
            
            
            


# test

if __name__ == '__main__':
    playList1_dict = {"song1":"Anti-Hero", "song2":"Hold Me Closer", "song3":"Super Freaky Girl", "song4":"Die For You"}
    
    playList1=PlayList(playList1_dict)
    
    print(playList1.song1)