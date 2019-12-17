import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import os
from src.imports import *
from src.connectors import cosmos
from time import time
import pandas as pd


from config import (
        DATA_FILENAME,
        DATA_FOLDER
        )

def init_():
    # global DB
    # DB = mongo.mongo_connect()
    # print('Initializing data')
    # start = time()

    connect_string='mongodb://w2c-healthcheck:fXhZ7CvUSHN6L18MtNS86SoaHbe20BB3yQxPzGmLGGnVGWMh4e63a2l3YSFK94Qvc9MmsyfLMVw8GWDxUBOxng==@w2c-healthcheck.documents.azure.com:10255/?ssl=true&replicaSet=globaldb'
    global DB
    DB = cosmos.get_database(connect_string,'testsite')
    print('Initializing data')


### load label map
# Label map contains metadata about the labels, like the label in vietnamese,
# color code for this label to show
#labels_list = ['DG','DX','HB','LN','LC','OT']
df_label_map = pd.read_csv((DATA_FOLDER/'label_map.csv').str())
#df_label_map = df_label_map[df_label_map.Code.isin(labels_list)].reset_index(drop=True)


### load label map
# Label map contains metadata about the labels, like the label in vietnamese,
# color code for this label to show
#labels_list = ['DG','DX','HB','LN','LC','OT']

#df_label_map = df_label_map[df_label_map.Code.isin(labels_list)].reset_index(drop=True)


    


    

