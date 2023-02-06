# importing libraries
import os 
from google.cloud import storage
import os
import openai
from dotenv import load_dotenv
from gpt_index import Document
from gpt_index import GPTSimpleVectorIndex
from gpt_index import (
    LLMPredictor
)
from langchain import OpenAI


# set up google client with credentials, open ai
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/maya.json'
storage_client = storage.Client()
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# variables to run script - these will be the arguments to run script
bucket_name = "maya-ai-demo-datasets"
folder = 'kalepa-dataset'
 
# function to get all buckets in project 
def list_buckets():
    try:
        buckets = storage_client.list_buckets()
        return buckets
    except Exception as e:
        print(f'Error listing buckets: {e}')
        return e      

# function to list blobs in bucket
def list_blobs(bucket_name,prefix):
    try:
        blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter='/')
        return blobs
    except Exception as e:
        print(f'Error listing blobs in bucket: {e}')
        return e 

# function to download a blob
def download_blob(bucket_name,file_name_bucket,file_name_local):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name_bucket)
        blob.download_to_filename(file_name_local)
        return True
    except Exception as e:
        return False   

# function main  
def main_script(bucket_name,folder):
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
            blobs_in_bucket = []
            prefix = folder+'/'
            blobs = list_blobs(bucket_name, prefix)
            for blob in blobs:
                blobs_in_bucket.append(blob.name)
                blob_name = blob.name
                split_name = blob_name.split('/')
                file_name = split_name[1]
                print(file_name)
            #for index, blob in enumerate(blobs_in_bucket):
                #download_blob(bucket_name,blob,'data/file'+str(index)+'.txt')
        else:
            print('Bucket does not exist in project, end of process')
    except Exception as e:
        print(f'Error executing main: {e}')   

if __name__ == "__main__":
    main_script(bucket_name,folder)