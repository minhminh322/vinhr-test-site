import dash
import dash_html_components as html
import dash_core_components as dcc
import time
from appnha import app
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("Introduction"),
                    html.P("Introduce about the test site")
                ], 

                style = {'padding' : '50px' , 
                    'backgroundColor' : '#fff'}),

                html.Div([
                    html.H1("Model Test"),
                    html.P("Introduce about Model Test feature")
                ],

                style = {'padding' : '50px' , 
                    'backgroundColor' : '#fff'}),

                html.Div([
                    html.H1("Model Ranking List"),
                    html.P("Introduce about Model Ranking list feature")
                ],     

                

                style = {'padding' : '50px' , 
                    'backgroundColor' : '#fff'}),
            ])

