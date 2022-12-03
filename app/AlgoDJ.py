import dash
import pickle
from dash import dcc, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from pathlib import Path
import dash_bootstrap_components as dbc
from viz.header import Header
from viz.user_input_row1 import UserInput1
from viz.user_input_row3 import UserInput3
from viz.wordcloudviz import WordCloudViz
from viz.timelineviz import TimeLineViz
from viz.network_graph import NetworkGraph
from viz.user_input_row1 import *
from viz.user_input_row3 import *
from model.track_network import TrackNetwork

with open(Path(Path.cwd(), "data","pickle_data", "songsample.pickle"), "rb") as f:
    user_input = pickle.load(f)

track_network = TrackNetwork(limit=10, num_songs=5, num_related=3)
recs = track_network.get_recommendations(user_input)
network = track_network.build_network(recs, "track")
playlist = track_network.get_playlist(recs, num_songs=10)
networkgraph = NetworkGraph(user_input).networkgraphapp
wordcloud = WordCloudViz(user_input).wordcloudapp
timeline = TimeLineViz(user_input).timelineapp

app = dash.Dash(__name__ ,external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])
server = app.server

UserInput2 = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Label("Title"),
            dbc.Input(id = "title", placeholder="Valid input...", valid=True, className="mb-3"),
        ],width={"size":9,"order":1}),
        dbc.Col([
            dbc.Label("Song sample"),
            dbc.Button(id ="song-sample",
            children = "Upload",
            color="primary",
            href="/",
            external_link=True,
            ),
        ],width={"size":3,"order":2})
    ]),

    dbc.Row([
        dcc.Upload(html.A('Upload File')),

        html.Hr(),

        dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File')
        ], style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    })
    ]),

    html.Br(),
    dcc.Store(id="store-data2", data=[], storage_type="memory")

])

app.layout = dbc.Container([
    html.Div([dbc.Container([
dbc.Row([Header]),
dbc.Row([
    dbc.Col([dbc.Row([dbc.Row([UserInput1, UserInput2, UserInput3])]), dbc.Row([wordcloud])]),
    dbc.Col([dbc.Row([networkgraph]), dbc.Row([timeline])])
    ]),
dcc.Store(id="store-data", data=[], storage_type="memory"),
html.Div(id="hidden", style={"display": "none"})
])])
])


@app.callback(
    Output("hidden", "children"),
    Input("song-sample", "n_clicks"),
    State("title", "value")
)
def update_song(n_clicks, ui):
    if ui is not None:
        with open(Path(Path.cwd(), "data","pickle_data", "songsample.pickle"), "wb") as f:
            pickle.dump(ui, f) 
        networkgraph = NetworkGraph(ui).networkgraphapp
        wordcloud = WordCloudViz(ui).wordcloudapp
        timeline = TimeLineViz(ui).timelineapp
        UserInput2 = html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Title"),
                            dbc.Input(id = "title", placeholder=ui, valid=True, className="mb-3"),
                        ],width={"size":9,"order":1}),
                        dbc.Col([
                            dbc.Label("Song sample"),
                            dbc.Button(id ="song-sample",
                            children = "Upload",
                            color="primary",
                            href="/",
                            external_link=True,
                            ),
                        ],width={"size":3,"order":2})
                    ]),

                    dbc.Row([
                        dcc.Upload(html.A('Upload File')),

                        html.Hr(),

                        dcc.Upload([
                        'Drag and Drop or ',
                        html.A('Select a File')
                        ], style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                    })
                    ]),
                    html.Br(),
                    dcc.Store(id="store-data2", data=[], storage_type="memory")
                ])
        app.layout = dbc.Container([
            html.Div([dbc.Container([
        dbc.Row([Header]),
        dbc.Row([
            dbc.Col([dbc.Row([dbc.Row([UserInput1, UserInput2, UserInput3])]), dbc.Row([wordcloud])]),
            dbc.Col([dbc.Row([networkgraph]), dbc.Row([timeline])])
            ]),
        dcc.Store(id="store-data", data=[], storage_type="memory"),
        html.Div(id="hidden", style={"display": "none"})
        ])])
        ])
        return ui
    return ui

if __name__ == '__main__':
    app.run_server(debug=True, threaded=False, use_reloader=False, port=8050)
    
    


