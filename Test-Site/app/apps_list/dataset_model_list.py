from _plotly_future_ import v4_subplots
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go

from datetime import datetime
from src.connectors import cosmos
from collections import OrderedDict
# from queue import Queue 
  
import dash_table
import pandas as pd
from src.connectors import cosmos, storage
import os
import flask
import DATA
import logging
from appnha import app
from apps_list import home
from dash.exceptions import PreventUpdate

from config import (
        DATA_FOLDER
        )

dataset_df = cosmos.get_table(DATA.DB, 'dataset_table')
model_df = cosmos.get_table(DATA.DB, 'model_table')
#sort id in ascending
dataset_df = dataset_df.sort_values('_id')
model_df = model_df.sort_values('_id')

# Initializing a queue
recall_queue = []

tables_row = html.Div([
                html.Div([

                    dbc.Row(dbc.Col(html.Div("Dataset List"), width=6)),
                
                    dash_table.DataTable(
                        id='dataset_table',

                        data=dataset_df.to_dict('records'),

                        columns=[{'id': c, 'name': c} for c in dataset_df.columns],

                        editable=True,
                        # sort_action='native',
                        # filter_action="native",
                        row_selectable="single",
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
                        style_as_list_view=True,
                    ),       
                ], className='dataset-row'),

                html.Div([

                    dbc.Row(dbc.Col(html.Div("Model List"), width=6)),
                
                    dash_table.DataTable(
                        id='model_table',

                        data=model_df.to_dict('records'),

                        columns=[{'id': c, 'name': c} for c in model_df.columns],

                        editable=True,
                        # sort_action='native',
                        # filter_action="native",
                        row_selectable="single",
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
                        style_as_list_view=True,
                    ),       
                ], className='model-row'),
    ], className='tables-row')


test_button = dbc.Button(
        "Test", 
        color="success",
        id='test-button',
        disabled='True', 
        className="test-button")

test_with_link = html.Div([ 
    html.A(test_button, href='/model-test', target="_blank")])

# Check availability
check_aval = html.Div([
            dbc.Button("Check Availability", id="open-centered"),
            dbc.Modal(
            [
                dbc.ModalHeader("Check Availability Status"),
                dbc.ModalBody(
                    html.P(
                      
                        id='modal-body',
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-centered", className="ml-auto"
                    )
                ),
            ],
            id="modal-centered",
            centered=True,
        ),
])

# History list
list_group = html.Div(
    [
        html.P('History List'),
        dbc.ListGroup(
            [
                # dbc.ListGroupItemHeading("History List"),
                dbc.ListGroupItem(
                    html.P(id="last-test-1"),
                    # color="success"
                ),
            ]
        ), 
    ]
)

layout = html.Div([
    tables_row, 
    html.Br(),
    dbc.Row(dbc.Col(check_aval, width=3),justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(test_with_link, width=2),justify="center"),
    html.Br(),
    dbc.Row(dbc.Col(list_group, width=6),justify="center"),
])


# Action when click on Test button
@app.callback(
    [Output('data-memory', 'data'),
    Output('model-memory', 'data')],
    [Input('open-centered', 'n_clicks')],
    [State('dataset_table', 'selected_rows'),
     State('model_table', 'selected_rows')]
)
def output_text(n_clicks, ds_row, mo_row):
    if not (ds_row or mo_row):
        raise PreventUpdate

    df_dataset = cosmos.query(DATA.DB['dataset_table'], {'_id': int(ds_row[0])})
    df_model = cosmos.query(DATA.DB['model_table'], {'_id': int(mo_row[0])})

    return df_dataset.to_json(date_format='iso', orient='split'), df_model.to_json(date_format='iso', orient='split')


# For check availability
@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('modal-body', 'children'),
    [Input('modal-centered', 'is_open')],
    [State('dataset_table', 'selected_rows'),
     State('model_table', 'selected_rows')]
)
def modal_notification(is_open, ds_row, mo_row):
    if is_open:
        if not (ds_row or mo_row):
            return[
                html.P("Please make your choice!!!!")
            ]

        # Insert user's choice to ranking table
        result_data = cosmos.query(DATA.DB['result_table'], 
        {'_id_dataset': ds_row[0],
        '_id_model': mo_row[0]})

        if result_data.empty:
            return [
            html.P('This dataset is currently unavailable')
            ]
        else:
            return [
            html.P('Your dataset is ready. Click Test button to continue')
            ]

@app.callback(
    Output('test-button','disabled'),
    [Input('modal-body','children')]
)
def toggle_test_button(status):
    if not status:
        raise PreventUpdate

    # Get the string inside model-body
    status_str = status[0]['props']['children']
    if status_str == 'Your dataset is ready. Click Test button to continue':
        return False
    return True

@app.callback(
    Output('recall-memory', 'data'),
    [Input('test-button', 'n_clicks')],
    [State('dataset_table', 'selected_rows'),
     State('model_table', 'selected_rows')]
)
def save_history(n_clicks, ds_row, mo_row):
    if not (ds_row or mo_row):
        raise PreventUpdate
    
    if len(recall_queue) > 2:
        recall_queue.pop(0)
    
    print(recall_queue)
    if n_clicks:
        recall_queue.append(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')+
            f": You've selected Dataset_ID: {ds_row[0]} and Model_ID: {mo_row[0]}")
    
    print(recall_queue)
    return recall_queue


# Display history test
@app.callback(
    Output('last-test-1','children'),
    [Input('recall-memory', 'data')]
)
def display_history(data_queue):
    if not data_queue:
        raise PreventUpdate

    length = len(data_queue)
    if length == 1:
        return html.P(data_queue[0])
    elif length == 2:
        return [
            html.P(data_queue[0]),
            html.P(data_queue[1])
        ]
    else:
        return [
            html.P(data_queue[0]),
            html.P(data_queue[1]),
            html.P(data_queue[2])
        ]
# Save prediction dataframe to memory
@app.callback(
    Output('prediction-memory', 'data'),
    [Input('data-memory', 'data')]
)
def save_df_prediction(data_json):
    if data_json is None:
        raise PreventUpdate

    #Unpack data from user's choice
    df_dataset = pd.read_json(data_json, orient='split')
    data_filename = df_dataset.loc[0, 'data_filename']


    # go to Azure storage
    client = storage.azure_client()
    # check if dataset is already downloaded
    if os.path.isfile(f'./static/prediction/{data_filename}') == False:
        storage.download_blob_to_folder(client, 'prediction', data_filename)
    
        ### predictions
    prediction_path = (DATA_FOLDER/'prediction'/data_filename)

    # print(prediction_path)
    # load df_pred
    df_pred = pd.read_csv(prediction_path.str())

    return df_pred.to_json(date_format='iso', orient='split')

# Highlight the selected row
@app.callback(
    Output('dataset_table', 'style_data_conditional'),
    [Input('dataset_table', 'selected_rows')]
)
def update_styles(selected_rows):
    return [{
        'if': { 'row_index': i },
        'background_color': '#D2F3FF'
    } for i in selected_rows]

@app.callback(
    Output('model_table', 'style_data_conditional'),
    [Input('model_table', 'selected_rows')]
)
def update_styles(selected_rows):
    return [{
        'if': { 'row_index': i },
        'background_color': '#D2F3FF'
    } for i in selected_rows]
