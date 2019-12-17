import dash
import dash_html_components as html
import dash_core_components as dcc
import time
from appnha import app
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


layout = html.Div(
    [
        dbc.Input(id="input", placeholder="Type something...", type="text"),
        html.Br(),
        html.P(id="output_test123"),
    ]
)


# @app.callback(Output("output_test", "children"), [Input("input", "value")])
# def output_text(value):
#     return value