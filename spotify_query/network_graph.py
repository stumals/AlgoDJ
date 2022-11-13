import os
import dash_cytoscape as cyto
from dotenv import load_dotenv
from spotify_artist_network import ArtistNetwork
from dash import Dash, html

load_dotenv()

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')


app = Dash(__name__)

artistnetwork = ArtistNetwork(artist='Polyphia', client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
artist_data = artistnetwork.sp.search(q=artistnetwork.artist, type='artist')
artistid = artist_data['artists']['items'][0]['id']
artist_tuples = [(artistid, artistnetwork.artist)]
artist_tuples += artistnetwork.get_related_artists(artistid)

connections = []

for artist_lvl_one in artist_tuples[1:]:
    artistnetwork = ArtistNetwork(artist=artist_lvl_one[1], client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    artist_data = artistnetwork.sp.search(q=artistnetwork.artist, type='artist')
    artistid = artist_data['artists']['items'][0]['id']
    next_level = artistnetwork.get_related_artists(artistid)
    connections.append((artist_tuples[0][0], artist_lvl_one[0]))
    for artist_lvl_two in next_level[1:]:
        idx = len(artist_tuples)
        artist_tuples += artistnetwork.get_related_artists(artistid)
        connections.append((artist_tuples[idx][0], artist_lvl_two[0]))

coords = [(i, i+1) for i in range(len(artist_tuples))]

init_artist_tuples = [(artist_tuples[_][0], artist_tuples[_][1], coords[_][0], coords[_][1]) for _ in range(len(coords))]

# for artist in artist_tuples[1:]:
# recast artist tuples to include coordinate for plot
        

    # artist_tuples = [(artistid, artistnetwork.artist)]
    # artist_tuples += artistnetwork.get_related_artists(artistid)

nodes = [
    {
        'data': {'id': short, 'label': label},
        'position': {'x': 10 * lat, 'y': -10 * long}
    }
    for short, label, long, lat in init_artist_tuples
]


edges = [
    {'data': {'source': source, 'target': target}}
    for source, target in connections
]

elements = nodes + edges

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-layout-1',
        elements=elements,
        style={'width': '100%', 'height': '500px', 'fill': 'steelblue'},
        stylesheet=[
            {
                'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'background-color': 'red'
                    }
            }],
        layout={
            'name': 'concentric',
            'minNodeSpacing': 40,
        }
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)