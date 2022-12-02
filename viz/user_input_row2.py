

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Dash, html, dcc, Input, Output, State




app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])


Genre = ["Pop", "Classic", "Country", "Jazz"]

# app.layout = dbc.Container([
UserInput2 = html.Div([

    dbc.Row([
        dbc.Col([
            dbc.Label("Title"),
            dbc.Input(id = "title", placeholder="Valid input...", valid=True, className="mb-3"),
        ],width={"size":9,"order":1}),
        dbc.Col([
            dbc.Label("Song sample"),
            dcc.Upload(dbc.Button(id ="song-sample",
            children = "Upload...",
            href="/static/data_file.txt",
            download="my_data.txt",
            external_link=True,
            color="primary",
            )),
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



# if __name__ == '__main__':
    # app.run_server('0.0.0.0',debug=True, threaded=False, use_reloader=False, port=8010)
