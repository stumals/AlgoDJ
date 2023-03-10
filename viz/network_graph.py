import dash_cytoscape as cyto
from dash import Dash, html
from model.track_network import TrackNetwork

# Load extra layouts
cyto.load_extra_layouts()

class NetworkGraph():
    def __init__(self, songsample):
        self.app = Dash(__name__)

        track_network = TrackNetwork(limit=10, num_songs=5, num_related=3)
        recs = track_network.get_recommendations(songsample)
        network = track_network.build_network(recs, "track")

        nodes = [
            {
                'data': {'id': node[0], 'label': node[1]},
            }
            for node in network.nodes()
        ]

        rootnode = nodes[0]["data"]["label"]

        edges = [
            {'data': {'source': connection[0][0], 'target': connection[1][0]}}
            for connection in network.edges()
        ]

        elements = nodes + edges

        self.networkgraphapp = cyto.Cytoscape(
                id='network-graph',
                elements=elements,
                style={'width': '100%', 'height': '370px'},
                stylesheet=[
                    {
                        'selector': 'node',
                            'style': {
                                'content': 'data(label)',
                                'height': 20,
                                'width': 20,
                                'background-color': '#30c9bc',
                                'color': '#ffffff'                               
                            }
                    },
                    {  
                        'selector': 'edge',
                            'style': {
                                'curve-style': 'haystack',
                                'haystack-radius': 0,
                                'width': 5,
                                'opacity': 0.5,
                                'line-color': '#a8eae5'
                                }
                    },
                    {
                        "selector": f'[label ^= "{rootnode}"]',
                        "style": {
                            "background-color": "maroon",
                            }
                    },
                    {
                        "selector": ":selected",
                        "style": {
                            "background-color": "steelblue",
                            "line-color": "steelblue",
                            "target-arrow-color": "steelblue",
                            "source-arrow-color": "steelblue"
                        }
                    }
                    ],
                layout={
                    'name': 'concentric',
                    'minNodeSpacing': 75,
                    'animate': False,
                }
            )

        # if __name__ == "__main__":
        #     app.run_server(debug=True)