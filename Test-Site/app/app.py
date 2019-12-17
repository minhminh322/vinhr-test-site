import DATA
DATA.init_()

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from src import helpers
from apps_list import home, model_test, model_ranking, dataset_model_list, help
from src.utils import navbar
# from src.connectors import mongo
from dash.exceptions import PreventUpdate
from appnha import app, server

app.layout = html.Div([
    # Store and share data between apps
    dcc.Store(id='data-memory', storage_type = 'local'),
    dcc.Store(id='model-memory', storage_type = 'local'),
    # dcc.Store(id='get-ids-memory', storage_type='local'),
    dcc.Store(id='prediction-memory', storage_type = 'local'),
    dcc.Store(id='recall-memory'),
    # dcc.Store(id='dataset-memory', storage_type = 'local'),
    dbc.Container([
        navbar.layout,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        ], fluid=True)
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/data-n-model-list':
        # dataset_model_list.init()
        return dataset_model_list.layout
    elif pathname == '/model-test':
        return model_test.layout
    elif pathname == '/model-ranking':
        return model_ranking.layout 
    elif pathname == '/help':
        return help.layout 
    else: 
        return dataset_model_list.layout

if __name__ == '__main__': 

    # app.run_server(port=80, host="0.0.0.0", debug=True)
    app.run_server(port = 8080, debug=True)

