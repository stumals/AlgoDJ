from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from model.track_network import TrackNetwork


class PlaylistTable():
    def __init__(self, songsample):
        self.app = Dash(__name__)

        track_network = TrackNetwork(limit=10, num_songs=5, num_related=3)
        recs = track_network.get_recommendations(songsample)
        network = track_network.build_network(recs, "track")
        playlist = track_network.get_playlist(recs, num_songs=10)
        df = playlist[['name', 'artists']].reset_index(drop=True)
        df['artists'] = df['artists'].astype(str)

        self.app.layout = dash_table.DataTable(df.to_dict('records'), 
                                        [{"name": str(i), "id": str(i)} for i in df.columns],
                                        style_table={'overflowX': 'auto'},
                                        style_cell={
                                            'height': 'auto',
                                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                                            'whiteSpace': 'normal', 'textAlign': 'left'},
                                        style_header={
                                            'backgroundColor': 'rgb(30, 30, 30)',
                                            'color': 'white'
                                        },
                                        style_data={
                                            'backgroundColor': 'rgb(50, 50, 50)',
                                            'color': 'white'
                                        }

                                        )

# if __name__ == '__main__':
#     app.run_server(debug=True)