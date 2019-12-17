from src.imports import *
import pandas as pd
import numpy as np
import DATA
import pandas as pd
from datetime import datetime, timedelta


def ct2ctts(ct, time_str):
    """Current Video Time to Current timestamp
    Arugments:
        ct (int|float) : 
            Current time of video that return from Video player.
        video_starttime (pd.Datetime) : 
            The starttime of video session in timestamp
    """
    # Video_starttime is used as anchor to find the timestamp 
    video_starttime = datetime.strptime(time_str, '%Y%m%d_%H%M%S')
    video_starttime = pd.to_datetime(video_starttime).tz_localize('Asia/Saigon')

    if ct is None: return None
    ctts = video_starttime + timedelta(seconds = int(ct))
    return ctts


def find_near_time_row(df, time, time_col = 'Timestamp'):
    """ Find the row has the time nearest to the argument time 
    Args : 
        df (pd.DataFrame): The data frame to find
        time (pd.Datetime): The reference time to find the nearest row
        time_col (str) : The name of time column in df
    Return : 
        index (int) : Index of the row has been found id df
        row (pd.Series) : That row
    """
    if time:
        time += timedelta(seconds=2)# offset time to make the UI looks like realtime

        # has to use Timestamp as index to use get_loc
        df = df.copy().set_index(time_col)

        index = df.index.get_loc(time,"nearest")
        row = df.iloc[index]
        row.ts = row.name # assign timestamp to ts
        diff_sec = abs((row.name - time).total_seconds())
        if diff_sec < 3 : 
            logging.info(f"Row found {row.name} with time {time}")
            return index+1, row
    logging.info(f"Row not found at {time} Min time {df.index[0]} Max {df.index[-1]}")
    return None, None


def segment(df_pred):
    """Segment the continuous label to a dataframe contains the count of each label over time
    """
    df = df_pred.copy() # avoid overwrite on the original dataframe
    prob_dict = dict(zip(df.Timestamp, df.Prob))

    # Find continuous label blocks
    df['Block'] = (df.Label.shift(1) != df.Label).astype(int).cumsum()
    count  = df.groupby(['Block','Label'])['Timestamp'].apply(list)

    df_count = pd.DataFrame(count).reset_index()
    # find len of each label blocks
    df_count['count'] = df_count.Timestamp.apply(len)
    df_count['Starttime'] = df_count['Timestamp'].apply(lambda x : x[0])
    df_count['Endtime'] = df_count['Timestamp'].shift(-1).apply(
        # Start time of next label is the end time of current label
        lambda x : x[0] if isinstance(x, list) else x)

    # shift will left one NaT at last, fill it with the max
    df_count['Endtime'].iloc[-1] = df['Timestamp'].max()


    # Map the probability
    df_count['Prob'] = df_count['Endtime'].map(prob_dict) # TODO :change this to mean

    #df_count.drop(['Block','Timestamp'], inplace=True, axis=1) # don't know why it fails when drop this

    return df_count

# def read_selected_ids(id=0):
#     # read from the user's choice in data and model list page
#     id_data = open('./static/data/get_id.txt', 'r').read()\
#             .replace('[','').replace(']','')

#     dataset_id = id_data.split('_')[0]
#     model_id = id_data.split('_')[1]
#     if id==0 and dataset_id:
#         return dataset_id 
#     elif id==1 and model_id:
#         return model_id 
#         # dataset_df = mongo.mongo_query(DATA.DB['dataset_table'], {'_id': int(dataset_id)})
#         # model_df = mongo.mongo_query(DATA.DB['model_table'], {'_id': int(model_id)})
#         # return dataset_df, model_df
#     else: return None

# # DUPLICATED CODE - NEED ACTION
# def get_dataset_filename():
#     dataset_id = read_selected_ids(0)
#     dataset_df = mongo.mongo_query(DATA.DB['dataset_table'], {'_id': int(dataset_id)})
#     return dataset_df.iloc[0]['data_filename']

# def get_video_filename():
#     dataset_id = read_selected_ids(0)
#     dataset_df = mongo.mongo_query(DATA.DB['dataset_table'], {'_id': int(dataset_id)})
#     return dataset_df.iloc[0]['video_filename']



