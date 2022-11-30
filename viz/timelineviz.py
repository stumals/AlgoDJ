
import pdb
import plotly.express as px
import dash
from dash import dcc, html
import plotly.graph_objects as go
from model.model_cosine_similarity import SongRecommender
from data.dataset import LoadData
from model.network import Network

track_network = Network(limit=20, num_songs=10, num_related=3)
recs = track_network.get_recommendations('Gimmie Trouble')
playlist = track_network.get_playlist(recs, num_songs=10)

fig = go.Figure(px.histogram(playlist, x = 'release_date', color = 'explicit', title = 'Date Distribution of Songs in Playlist'))
fig.update_layout(bargap = 0.2)

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure = fig)
])
app.run_server(debug = True, use_reloader = False)