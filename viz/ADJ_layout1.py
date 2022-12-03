import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from viz.header import Header
from viz.user_input_row1 import UserInput1
# from viz.user_input_row2 import UserInput2
from viz.user_input_row3 import UserInput3
from viz.wordcloudviz import WordCloudViz
from viz.timelineviz import TimeLineViz
from viz.network_graph import NetworkGraph
from viz.user_input_row1 import *
# from viz.user_input_row2 import *
from viz.user_input_row3 import *
from model.track_network import TrackNetwork

user_input = "Calm Like a Bomb"

track_network = TrackNetwork(limit=10, num_songs=5, num_related=3)
recs = track_network.get_recommendations(user_input)
network = track_network.build_network(recs, "track")
playlist = track_network.get_playlist(recs, num_songs=10)
networkgraph = NetworkGraph(user_input).networkgraphapp
wordcloud = WordCloudViz(user_input).wordcloudapp
timeline = TimeLineViz(user_input).timelineapp

app = dash.Dash(__name__ ,external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])

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
            # href="/static/data_file.txt",
            # download="my_data.txt",
            # external_link=True,
            color="primary",
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

ADJ_Layout = dbc.Container([
dbc.Row([Header]),
dbc.Row([
    dbc.Col([dbc.Row([dbc.Row([UserInput1, UserInput2, UserInput3])]), dbc.Row([wordcloud], id="word-cloud")]),
    dbc.Col([dbc.Row([networkgraph], id="network-graph"), dbc.Row([timeline], id="time-line")])
    ]),
dcc.Store(id="store-data", data=[], storage_type="memory")
])

@app.callback(
    # Output("first_output_1", "children"),
    Output("network-graph", "figure"),
    Output("word-cloud", "figure"),
    Output("time-line", "figure"),
    Input("song-sample", "n_clicks")
)
def change_text(user_input):
    # recs = track_network.get_recommendations(user_input)
    # network = track_network.build_network(recs, "track")
    # playlist = track_network.get_playlist(recs, num_songs=10)
    networkgraph = NetworkGraph(user_input).networkgraphapp
    wordcloud = WordCloudViz(user_input).wordcloudapp
    timeline = TimeLineViz(user_input).timelineapp
    return networkgraph, wordcloud, timeline
    
    # ADJ_Layout = dbc.Container([
    # dbc.Row([Header]),
    # dbc.Row([
    #     dbc.Col([dbc.Row([dbc.Row([UserInput1, UserInput2, UserInput3])]), dbc.Row([wordcloud])]),
    #     dbc.Col([dbc.Row([networkgraph]), dbc.Row([timeline])])
    #     ]),
    # dcc.Store(id="store-data", data=[], storage_type="memory")
    # ])
    # return ADJ_Layout




# def init_input_layout1_callbacks(app):

#     @app.callback(
#         Output(component_id="row1_validation",   component_property="children"),
#         Input(component_id= "from",              component_property="value"),
#         Input(component_id= "to",                component_property="value"),
#         Input(component_id= "playlist-size",     component_property="value"),
#         prevent_initial_call = True
#     )
#     # def validate_values(year_from, year_to, playlist_size):

#     #     if (year_from is None) or (year_to is None):
#     #         pass
#     #         # raise PreventUpdate
#     #     elif int(year_from) >= int(year_to):
#     #         # return 'Alert: Start year must be smaller than end year!'
#     #         return dbc.Alert("Alert: Start year must be smaller than end year!", color="warning")
#     #     elif playlist_size is None:
#             # return 'Alert: Please select playlist size!'
#             # return dbc.Alert("Please select playlist size!", color="warning")



#     @app.callback(
#         Output(component_id="store-data",    component_property="data"),
#         [Input(component_id="enter",         component_property="n_clicks")],
#         [State(component_id="playlist-size", component_property="value"),
#         State(component_id="from",          component_property="value"),
#         State(component_id="to",            component_property="value"),
#         State(component_id="genre",         component_property="value"),
#         State(component_id="title",         component_property="value"),
#         State(component_id="song-sample",   component_property="value"),
#         State(component_id="age",           component_property="value"),
#         State(component_id="gender",        component_property="value")],
#         prevent_initial_call = True
#     )
#     # def extract_user_data(n_clicks, playlist_size, yr_from, yr_to, genre, title, song_sample, age, gender)->list:
#     #     data = {"playlist_size" : [playlist_size],
#     #             "yr_from"       : [yr_from],
#     #             "yr_to"         : [yr_to],
#     #             "genre"         : [genre],
#     #             "title"         : [title],
#     #             "song_sample"   : [song_sample],
#     #             "age"           : [age],
#     #             "gender"        : [gender]}
#     #     print(data)
#     #     user_data = data
#     #     return [data]




#     @app.callback(
#         [Output(component_id="playlist-size",  component_property="value"),
#         Output(component_id="from",           component_property="value"),
#         Output(component_id="to",             component_property="value"),
#         Output(component_id="genre",          component_property="value"),
#         Output(component_id="title",          component_property="value"),
#         Output(component_id="age",            component_property="value"),
#         Output(component_id="gender",         component_property="value")],
#         Input(component_id="clear",            component_property="n_clicks")
#     )
    # def clear_layout_data(clear)-> None:
    #     return None , None, None, None, None, None, None


    # @app.callback(

    # )




# if __name__ == '__main__':
#     app.run_server(debug=True, threaded=False, use_reloader=False,port=8020)
    # app.run_server(debug=True)
