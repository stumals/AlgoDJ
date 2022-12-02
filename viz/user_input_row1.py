from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from app.classes import User

global data1




app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])



Genre = ["Pop", "Classic", "Country", "Jazz", "Rock", "Hard Rock", "Post-rock", "Metal", "Heavy metal", "Flamenco"]

# app.layout = dbc.Container([
UserInput1 = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("Playlist size"),
            dbc.Select( id = "playlist-size",
                options=[{"label": i, "value": i}
                    for i in range(2,37)]),
            ]),
        dbc.Col([
            dbc.Label("From"),
            dbc.Select( id = "from",
                options=[{"label": x, "value": x, "type":"number"}
                    for x in range(1950,2023)]),
        ]),
        dbc.Col([
            dbc.Label("To"),
            dbc.Select( id = "to",
                options=[{"label": y,"value": y, "type":"number",}
                    for y in range(1950,2023)]),
        ]),

        dbc.Col([
            dbc.Label("Genre"),
            dbc.Select( id = "genre",
                options=[{"label": i, "value": i}
                    for i in Genre]),
        ]),
        ]),
    html.Div(id="row1_validation"),
    html.Br(),
    dcc.Store(id="store-data1", data=[], storage_type="memory")

])

if __name__ == '__main__':
    app.run_server('0.0.0.0',debug=True, threaded=False, use_reloader=False, port=8010)
