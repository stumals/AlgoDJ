

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import Dash, html, dcc, Input, Output, State




app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])


Genre = ["Pop", "Classic", "Country", "Jazz"]

# app.layout = dbc.Container([
UserInput3 = html.Div([
        dbc.Row([
            dbc.Col([
            dbc.Label("Age"),
            dbc.Select( id = "age",
                options=[{"label": i, "value": i}
                    for i in range(10,100)]),
            ]),

        # ],width={"size":2,"order":1}),
        # dbc.Col([

        # ],width={"size":1,"order":2}),
        dbc.Col([
            html.Div([
                dbc.Label("Gender"),
                dbc.RadioItems(
                    options=[
                        {"label": "Male", "value": 1},
                        {"label": "Female", "value": 2},
                    ],
                    value=1,
                    id="gender",
                    inline=True,
            ),
            ])
        ]),
        # ],width={"size":1,"order":2}),

        dbc.Col([

        ],width={"size":1,"order":3}),

        dbc.Col([
            html.Br(),
            dbc.Button(id="enter" ,children="Enter", color="success", className="me-1", n_clicks=0),
        # ],width={"size":1,"order":4}),
        ]),
        # dbc.Col([

        # ],width={"size":1,"order":5}),


        dbc.Col([
            html.Br(),
            dbc.Button(id="clear" ,children="Clear", color="info",    className="me-1"),
        ]),
        # ],width={"size":1,"order":5}),
        dcc.Store(id="store-data3", data=[], storage_type="memory")

    ]),

        dbc.Row([
        dbc.Col([
            html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "#AB87FF","opacity": "unset"})
        ], width={"size":12,})
        ])
])








# if __name__ == '__main__':
    # app.run_server('0.0.0.0',debug=True, threaded=False, use_reloader=False, port=8010)
