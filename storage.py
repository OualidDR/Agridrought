import json
import os 
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient


load_dotenv()

def save_rains_json(data, filename="rainfall_total.json") :
    with open (filename, "w") as f :
        json.dump(data, f, indent= 2)

def load_to_azure_blob(file_name, blob_name) :
    
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service.get_container_client("bronze")
    blob_client = container_client.get_blob_client(blob_name)

    with open (file_name, "rb") as data :
        blob_client.upload_blob(data, overwrite=True)


def download_from_blob(blob_name, file_name):
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service.get_container_client("bronze")
    blob_client = container_client.get_blob_client(blob_name)

    with open(file_name, "wb") as data:
        download_stream = blob_client.download_blob()
        data.write(download_stream.readall())


def get_blob_client(container, blob_name):
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    service = BlobServiceClient.from_connection_string(connection_string)
    return service.get_container_client(container).get_blob_client(blob_name)

def upload_json(container, blob_name, obj):
    get_blob_client(container, blob_name).upload_blob(json.dumps(obj, indent=2), overwrite=True)

def download_json(container, blob_name):
    return json.loads(get_blob_client(container, blob_name).download_blob().readall())


