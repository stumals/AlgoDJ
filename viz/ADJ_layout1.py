from os import path
import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
from viz.header import Header
from viz.user_input_row1 import UserInput1
from viz.user_input_row2 import UserInput2
from viz.user_input_row3 import UserInput3
from viz.wordcloudviz import WordCloudViz
from viz.timelineviz import TimeLineViz
from viz.network_graph import NetworkGraph
from viz.user_input_row1 import *
from viz.user_input_row2 import *
from viz.user_input_row3 import *
from model.track_network import TrackNetwork

user_input = "Down on the Farm"

track_network = TrackNetwork(limit=10, num_songs=5, num_related=3)
recs = track_network.get_recommendations(user_input)
network = track_network.build_network(recs, "track")
playlist = track_network.get_playlist(recs, num_songs=10)
networkgraph = NetworkGraph(user_input).networkgraphapp
wordcloud = WordCloudViz(user_input).wordcloudapp
timeline = TimeLineViz(user_input).timelineapp


app = dash.Dash(__name__ ,external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])


ADJ_Layout = dbc.Container([
    dbc.Row([Header]),
    dbc.Row([
        dbc.Col([dbc.Row([dbc.Row([UserInput1, UserInput2, UserInput3])]), dbc.Row([wordcloud])]),
        dbc.Col([dbc.Row([networkgraph]), dbc.Row([timeline])])
        ]),
    # dbc.Row([
    #     dbc.Col([
    #         dbc.Row([UserInput1, UserInput2, UserInput3, wordcloud]),
    #         # dbc.Row([playlist]),
    #         ]),
    #     dbc.Col([networkgraph, timeline]),
    #     # dbc.Col([]),
    #     ]),
    dcc.Store(id="store-data", data=[], storage_type="memory")
])

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
