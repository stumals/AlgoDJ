import os
import dash_cytoscape as cyto
from dash import Dash, html
from model.track_network import TrackNetwork

# Load extra layouts
cyto.load_extra_layouts()

# load_dotenv()

# CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
# CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')


app = Dash(__name__)

track_network = TrackNetwork(limit=1000, num_songs=5, num_related=5, src="millions")
playlist = track_network.get_playlist("Saints Go Marching In")
network = track_network.build_network(track_network.songbank, playlist, "track")


nodes = [
    {
        'data': {'id': node[0], 'label': node[1]},
    }
    for node in network.nodes()
]


edges = [
    {'data': {'source': connection[0][0], 'target': connection[1][0]}}
    for connection in network.edges()
]

elements = nodes + edges

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-layout-1',
        elements=elements,
        style={'width': '100%', 'height': '500px'},
        stylesheet=[
            {
                'selector': 'node',
                    'style': {
                        'content': 'data(label)',
                        'background-color': 'steelblue'
                    }
            },
            {  
                'selector': 'edge',
                    'style': {
                        'width': 2
                        }
            }],
        layout={
            'name': 'breadthfirst',
            'minNodeSpacing': 120,
            'animate': False,
        }
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)