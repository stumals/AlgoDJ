"""app folder: Artist class
"""

 
 
class Artist(object):
    def __init__(self, artist_dict):
        for k in artist_dict:
            setattr(self, k, artist_dict[k])
            
            
            


# test

if __name__ == '__main__':
    artist1_dict = {"name":"Taylor Swift", "dob":"12-13-1989", "gender":"female", "Language":"English"}
    
    artist1=Artist(artist1_dict)
    
    print(artist1.gender)