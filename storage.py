import json
import os 
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient


load_dotenv()

def save_rains_json(rains) :
    with open ("rainfall_total.json", "w") as f :
        json.dump(rains, f, indent= 2)

def load_to_azure_blob(file_name, blob_name) :
    
    connection_string = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_service = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service.get_container_client("bronze")
    blob_client = container_client.get_blob_client(blob_name)

    with open (file_name, "rb") as data :
        blob_client.upload_blob(data, overwrite=True)







