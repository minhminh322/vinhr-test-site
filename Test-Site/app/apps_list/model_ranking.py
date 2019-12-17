from _plotly_future_ import v4_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go
from appnha import app
from src.connectors import cosmos
from collections import OrderedDict
import dash_table
import pandas as pd
import os
import flask
import DATA
import logging
from apps_list import home
 


# Dataframe model result from MongoDB
model_df = cosmos.get_table(DATA.DB, 'model_table')

ranking_col = html.Div([dash_table.DataTable(
    data=[{'rank':i} for i in range(1,4)],
    columns=[{'id':'rank','name': 'Rank'}],
                
                        selected_rows=[],
                        filter_action="native",
                        fixed_rows={ 'headers': True, 'data': 0 },

                        # Style
                        style_cell={'width': '150px', 'textAlign': 'center', 'padding': '5px'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        style_cell_conditional=[
                            {
                                'if': {'column_id': 'Region'},
                                'textAlign': 'center'
                            }
                        ],
)], style={'padding-top': '26%'})

tables_col = html.Div([
                    dash_table.DataTable(
                        id='model_table',
                        data=model_df.to_dict('records'),
                        columns=([{'id': c, 'name': c, "hideable": True} for c in model_df.columns]),

                        # editable=True,
                        sort_action='native',
                        filter_action="native",
                        # row_selectable="single",
                        hidden_columns=['_id'],
                        selected_rows=[],

                        fixed_rows={ 'headers': True, 'data': 0 },

                        # Style
                        style_cell={'width': '150px', 'textAlign': 'center', 'padding': '5px'},
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        style_cell_conditional=[
                            {
                                'if': {'column_id': 'Region'},
                                'textAlign': 'center'
                            }
                        ],
                        # style_as_list_view=True,
                    ),       
                ], className='model-result-row')
    
 
layout = html.Div([
    dbc.Row([
        dbc.Col(ranking_col, width=1),
        dbc.Col(tables_col, width=11),
    ], no_gutters=True,)
],)

