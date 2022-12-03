
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from model.model_cosine_similarity import SongRecommender
from data.dataset import LoadData
from model.network import Network

class TimeLineViz():
    def __init__(self, songsample):
        track_network = Network(limit=20, num_songs=10, num_related=3)
        recs = track_network.get_recommendations(songsample)
        playlist = track_network.get_playlist(recs, num_songs=10)

        fig = fig = go.Figure(px.histogram(playlist, x = 'release_date', template = 'plotly_dark',
                                    title = 'Date Distribution of Songs in Playlist',
                                    labels = {
                                        "release_date" : "Release Date",
                                    }))
        fig.update_layout({
            'bargap': 0.2,
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })

        # style = {'height': '300px', 'width': '540px'}

        self.app = dash.Dash()
        self.timelineapp = html.Div([
            dcc.Graph(figure = fig),
        ])
        # app.run_server(debug = True, use_reloader = False)