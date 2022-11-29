
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import plotly.graph_objects as go
from model.model_cosine_similarity import SongRecommender
from data.dataset import LoadData


df_raw = LoadData().get_data()


playlist = SongRecommender(df_raw, 'Gimmie Trouble').recommender()



fig = go.Figure(px.histogram(playlist, x = 'release_date', color = 'explicit', title = 'Date Distribution of Songs in Playlist'))
fig.update_layout(bargap = 0.2)


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig)
])
app.run_server(debug = True, use_reloader = False)