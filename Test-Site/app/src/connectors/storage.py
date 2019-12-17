import os, uuid, sys
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, BlobClient
from datetime import datetime, timedelta
from io import StringIO
import pandas as pd
# from azure.storage.filedatalake import DataLakeServiceClient

def azure_client():
    connect_str = "DefaultEndpointsProtocol=https;AccountName=vinhrstorage;AccountKey=eP0Zm7HogchL6nAsNBTaOE654/OEGbSqojUm28BgCqf97mUGfUyqHQEqVX73dKWjou3E5waaV0bn0+XaMAr6pQ==;EndpointSuffix=core.windows.net"

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str) 

    return blob_service_client  

def download_blob_to_folder(client, container_name, blob_name):

    blob_client = client.get_blob_client(container=container_name, blob=blob_name)
    # Create a file in local Documents directory to upload and download
    local_path = f"./static/{container_name}/"
    # download_file_path = os.path.join(local_path, blob_name)
    # print("\nDownloading blob to \n\t" + download_file_path)

    # Download the blob to a local file
    # Add 'DOWNLOAD' before the .txt extension so you can see both files in Documents
    download_file_path = os.path.join(local_path, blob_name)
    # print(os.path.exists(local_path))
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())   

def get_blob_url(client, container_name, blob_name):
    # Get sas_token for sharing videos
    sas_token = generate_account_sas(
        account_name="vinhrstorage",
        account_key="eP0Zm7HogchL6nAsNBTaOE654/OEGbSqojUm28BgCqf97mUGfUyqHQEqVX73dKWjou3E5waaV0bn0+XaMAr6pQ==",
        resource_types=ResourceTypes(object=True),
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=24)
    )
    source_blob = BlobClient(
                client.url,
                container_name=container_name,
                blob_name=blob_name,
                credential=sas_token)

    return source_blob.url



### DATALAKE
# global service_client

# def datalake_client():
#     storage_account_name = 'vinhrdatalake'
#     storage_account_key = 'WK8CdfdKlGlFhcYcfNNjcUHu8KxjviuZnKqmqyeSiQY6UzlSGcuy+cKbfgbjpm1ofwxAhfdQHzdYi1ZewWEQUA=='
#     service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
#         "https", storage_account_name), credential=storage_account_key)
#     return service_client

# def create_file_system(client):
#         file_system_client = client.create_file_system(file_system="my-file-system")
        

# def download_file_from_storage(client, directory, filename):

#         file_system_client = client.get_file_system_client(file_system="hkdata")

#         directory_client = file_system_client.get_directory_client("PredictionDataset/")
        
#         local_file = open("./download.csv",'wb')

#         file_client = directory_client.get_file_client("W_012 191024 14_39_30.csv")

#         downloaded_bytes = file_client.read_file()

#         local_file.write(downloaded_bytes)

#         local_file.close()


# client = datalake_client()
# download_file_from_storage(client)
# create_file_system(client)