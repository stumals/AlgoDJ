import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

def main():
    
    pl_uri = 'spotify:artist:1qQLhymHXFPtP5U8KNKsm6'

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    
    results = spotify.artist_top_tracks(pl_uri)
    for track in results['tracks'][:5]:
        print(f"track    : {track['name']}")
        print(f"audio    : {track['preview_url']}")
        print(f"cover art: {track['album']['images'][0]['url']}")
        print()
        
    recs = spotify.artist_related_artists(pl_uri)
    for person in recs['artists'][:5]: #returns related artists 
        print(f"You will also like {person.get('name')}.")
        print()
        
    albums = spotify.artist_albums(pl_uri)
    print(f"Top albums:") 
    for i, album in enumerate(albums.get('items')[:5]): #returns related albums
        print(f"{i+1}, {album.get('name')}.")    
    
    return



if __name__ == "__main__":
    main()