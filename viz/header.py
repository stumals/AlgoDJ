
from os import path
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import base64




# app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport', 'content': 'width=device-width,initial-scale=1.0'}])

resources_dir = path.join(path.dirname(__file__), 'img')
image_filename = '/playlist.png' # image
encoded_image = base64.b64encode(open(resources_dir+image_filename, 'rb').read())

Header = html.Div([
# app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '100%'})
            
        ], width={"size":1,"order":1}),
        
        dbc.Col([
            html.Br(),
            html.H1("AlgoDJ"),
            # html.H5('''Create your own playlist based on a song of your chosen'''),
            html.H5('''You got a song! AlgoDJ has a playlist for you!'''),
        ], width={"size":8,"order":2}),
        dbc.Col([
           
                html.Br(), 
                html.Br(),
                
            dbc.ButtonGroup(
                [
                    dbc.Button(id="sign_in" ,children="Sign in" ,  color="danger"),
                    dbc.Button(id="sign_out",children="Sign out", color="warning"),
                    dbc.Button(id="sign_up" ,children="Sign up" , color="success"),
                ], className="mb-4",),
        ], width={"size":3,"order":3}),
    ]), 
    dbc.Row([
        dbc.Col([
            html.Hr(style={'borderWidth': "2vh", "width": "100%", "borderColor": "#F3DE8A","opacity": "unset"})
        ], width={"size":12,})
    ])
 
])

# if __name__ == '__main__':
#     app.run_server('127.0.0.1',debug=True, threaded=False, use_reloader=False, port=8001)
#     app.run_server('0.0.0.0',debug=True, port=8001)
    
    
   