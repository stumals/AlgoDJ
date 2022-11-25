
from pathlib import Path
import pandas as pd
from data.dataset import LoadData
from dash_holoniq_wordcloud import DashWordcloud
from dash import Dash, html
from model.model_cosine_similarity import SongRecommender
from model.network import Network

df_raw = LoadData().get_data()
playlist = SongRecommender(df_raw, 'She Belongs to Me').recommender()

g = Network(limit=20, num_songs=10, num_related=3).build_network(df_raw, playlist, "artist")
#g.degree
#g.degree['Bob Dylan']


dicttolist = list(g.degree)
artists1 = [list(ele) for ele in dicttolist]
artists = artists1[0:10] #limiting to just ten artists in the word cloud for now for spacing
#artists


app = Dash(__name__)

# this was the dummy data that I was working with before getting
# the data from Stu's classes
# artists = [
#     ["Taylor Swift", 30],
#     ["The Rolling Stones", 20],
#     ["Red Hot Chili Peppers", 10],
#     ["The Beatles", 40],
#     ["Beyonce", 30],
#     ["Coldplay", 20],
#     ["Maroon 5", 20],
#     ["Foo Fighters", 10],
#     ["Zac Brown Band", 10],
#     ["O.A.R.", 10]
# ]

app.layout = html.Div([
    html.Div([
        DashWordcloud(
            id='wordcloud',
            list=artists,
            width=300, height=200,
            gridSize=16,
            color='#f0f0c0',
            backgroundColor='#001f00',
            shuffle=False,
            rotateRatio=0.5,
            shrinkToFit=True,
            shape='circle',
            hover=True
            )
        ])
    ])

if __name__ == '__main__':
    app.run_server('0.0.0.0',debug=True, threaded=True, use_reloader=True, port=8888)
