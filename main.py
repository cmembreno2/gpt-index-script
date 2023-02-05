# importing libraries
import os 
from google.cloud import storage
import os
import openai
from dotenv import load_dotenv
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader

# set up google client with credentials, open ai
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/credentials.json'
storage_client = storage.Client()
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# variables to run script - these will be the arguments to run script
bucket_name = "test-bucket-dataset-cm-1" 
 
# function to get all buckets in project 
def list_buckets():
    try:
        buckets = storage_client.list_buckets()
        return buckets
    except Exception as e:
        print(f'Error listing buckets: {e}')
        return e      

# function to list blobs in bucket
def list_blobs(bucket_name):
    try:
        blobs = storage_client.list_blobs(bucket_name)
        return blobs
    except Exception as e:
        print(f'Error listing blobs in bucket: {e}')
        return e    

# function main  
def main_script(bucket_name):
    try:
        # get buckets in project
        try:
            buckets_in_project = []
            buckets = list_buckets()
            for bucket in buckets:
                buckets_in_project.append(bucket.name)
        except Exception as e:
            print(f'Error trying to get buckets in project: {e}')
        # verify that required bucket exist in project
        bucket_exists = bucket_name in buckets_in_project 
        if bucket_exists:
            blobs = list_blobs(bucket_name)
            for blob in blobs:
                print(blob.name)
        else:
            print('Bucket does not exist in project, end of process')
    except Exception as e:
        print(f'Error executing main: {e}')   

if __name__ == "__main__":
    main_script(bucket_name)