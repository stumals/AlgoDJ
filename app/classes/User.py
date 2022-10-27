"""app folder: User class
"""

 
 
class User(object):
    def __init__(self, user_dict):
        for k in user_dict:
            setattr(self, k, user_dict[k])
            
            
            


# test

if __name__ == '__main__':
    user1_dict = {"name":"Roger Federer", "age":"41", "gender":"Male", "language":"English"}
    
    user1=User(user1_dict)
    
    print(user1.gender)