from pymongo import MongoClient
import pandas as pd

def get_database(connection_string: str, database: str) -> MongoClient:
    client = MongoClient(connection_string)
    database = client[database]
    return database


def insert(db_col, data_dict):
    db_col.insert_one(data_dict)

def query(db_col, query):
    cursor = db_col.find(query)
    df = pd.DataFrame(list(cursor))
    return df

def get_table(db_name, db_table):
    cursor = db_name[db_table].find()
    df = pd.DataFrame(list(cursor))
    return df


connect_string='mongodb://w2c-healthcheck:fXhZ7CvUSHN6L18MtNS86SoaHbe20BB3yQxPzGmLGGnVGWMh4e63a2l3YSFK94Qvc9MmsyfLMVw8GWDxUBOxng==@w2c-healthcheck.documents.azure.com:10255/?ssl=true&replicaSet=globaldb'
DB = get_database(connect_string,'testsite')
result_table = DB['result_table']
# dataset_table = DB['dataset_table']
# model_table = DB['model_table']
result_1 ={
    # '_id': 2,
    '_id_dataset': 1,
    '_id_model': 2,
    'accuracy': 0.01,
    'processing_time': 100,
    'TBD': '...'
}
result_table.insert_one(result_1)

# model_1 = {
#     '_id': 2,
#     'model_name': 'Gaussian',
#     'model_windowsize': 50,
#     'model_transformation': 'Scaling',
#     'processtime': 9,
#     'author': "ngockq",
#     'date': '25/11/2019',
#     'accuracy': 0.9,
#     'f1_score': 0.33,
# }
# model_table.insert_one(model_1)

# dataset_1 = {
#     '_id': 2, 
#     'data_filename':'W_012 191024 10_18_16.csv', 
#     'video_filename':'20191024_101819.MOV',
#     'frequency': 1,
#     'session_id': 4,
#     'hk_id': 2,
#     'hand': 'D',
#     'duration': '500',
#     'date': '23/11/2019',
#     'description': '',}
# dataset_table.insert_one(dataset_1)

# m_1 = {
#     '_id': 2,
#     '_id_dataset': 1,
#     '_id_model': 3,
#     'accuracy': 0.5,
#     'processing_time': 30,
#     'tbd': 'zzz'
# }
# result_table.insert_one(m_1)


# dataset_2 = {
#     '_id': 1, 
#     'data_filename':'W_012 191024 09_59_31.csv', 
#     'video_filename':'20191024_095933.MOV',
#     'date': '',
#     'description': ''}

# dataset_3 = {
#     '_id': 2, 
#     'data_filename':'W_012 191024 14_39_30.csv', 
#     'video_filename':'20191024_143935.MOV',
#     'date': '',
#     'description': ''}

# dataset_test = {
#     '_id': '4_1', 
#     'data_filename':'W_012 191024 14_39_30.csv', 
#     'video_filename':'20191024_143935.MOV',
#     'date': '',
#     'description': ''}

# model_1 = {
#     '_id': 0,
#     'Model'
# }

# ranking_table.insert_one(m_1)

# dataset_table.insert_many([dataset_1, dataset_2, dataset_3])
# result = dataset_table.find({})
# def get_dataset_table():
#     return dataset_table.find({})