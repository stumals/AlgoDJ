import dash_bootstrap_components as dbc 
from dash_holoniq_wordcloud import DashWordcloud
from dash import Dash, html
from model.network import Network

class WordCloudViz():
    def __init__(self, songsample):
        
        track_network = Network(limit=20, num_songs=10, num_related=3)
        recs = track_network.get_recommendations(songsample)
        g = track_network.build_network(recs, "artists")


        dicttolist = list(g.degree)
        artists1 = [list(ele) for ele in dicttolist]
        artists = artists1[0:20] #limiting to just ten artists in the word cloud for now for spacing
        maxval = 0
        sizeadjuster = 30
        for row in artists:
            if row[1] >= maxval:
                maxval = row[1]
            row[0] = row[0].replace('\'', '')
        for row in artists:
            row[1] = (row[1]/maxval) * sizeadjuster
        for row in artists:
            if row[1] <= 10:
                row[1] = 10
        print(artists)
        #artists


        self.app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], 
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])

        self.wordcloudapp = html.Div([
            html.Div([
                DashWordcloud(
                    id='wordcloud',
                    list=artists,
                    width=540, height=350,
                    gridSize=20,
                    color='#73AFB6',
                    backgroundColor='#222222',
                    shuffle=False,
                    rotateRatio=0.5,
                    shrinkToFit=True,
                    shape='circle',
                    hover=True
                    )
                ])
            ])


        # if __name__ == '__main__':
        #     app.run_server("127.0.0.1",debug=True, threaded=False, use_reloader=False, port=8050)