# importing libraries
import os 
from google.cloud import storage
import os
import openai
from dotenv import load_dotenv
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader

# set up google client with credentials, open ai
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
storage_client = storage.Client()
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# variables to run script - these are the argument to run script
directory = 'data'
index_name = 'indexes/index_call.json'
query = 'Please summarize the call'
bucket_name = 'test-bucket-dataset-cm-1'
file_name_bucket = 'kalepa-dataset/Copy of Copy of 2020 08 04 Copilot Intro demo for xpt.txt'
index_name_bucket = 'kalepa-dataset/index_call.json'
file_name_local= 'data/Copy of Copy of 2020 08 04 Copilot Intro demo for xpt.txt'  

# get all buckets in project 
def list_buckets():
    print(f'Executing function to list buckets in project')
    try:
        buckets = storage_client.list_buckets()
        for bucket in buckets:
            print(bucket.name)
        return True
    except Exception as e:
        print(f'Error listing buckets')
        return False      

# function to get the bucket
def get_bucket(bucket_name):
    try:
        print(f'Executing function to get the bucket with name: {bucket_name}')
        bucket = storage_client.bucket(bucket_name)
        print(f'Found bucket with name: {bucket.name}')
        return True
    except Exception as e:
        print(f'Error getting the bucket: {e}')
        return False

# function to list blobs in bucket
def list_blobs(bucket_name):
    print(f'Executing function to list blobs in bucket')
    try:
        blobs = storage_client.list_blobs(bucket_name)
        for blob in blobs:
            print(blob.name)
        return True
    except Exception as e:
        print(f'Error listing blobs in bucket')
        return False    
    
# function to download blob from bucket
def download_blob(bucket_name,file_name_bucket,file_name_local):
    print(f'Executing function to download blob from bucket')
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name_bucket)
        blob.download_to_filename(file_name_local)
        print("Saved")
        return True
    except Exception as e:
        print(f'Not saved: {e}')
        return False

# function to create index from file
def create_index(directory,index_name):
    print(f'Executing function to create index from file')
    try:
        documents = SimpleDirectoryReader(directory).load_data()
        index = GPTSimpleVectorIndex(documents)
        index.save_to_disk(index_name)
        return True
    except Exception as e:
        print(f'Error creating index: {e}')
        return False
    
# function to upload the index to bucket
def upload_index_to_bucket(index_name_bucket, index_name, bucket_name):
    print(f'Executing function to upload index')
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(index_name_bucket)
        blob.upload_from_filename(index_name)
        return True
    except Exception as e:
        print(f'Error uploading the index: {e}')
        return False    

# function to query from index
def query_index(index_name,query):
    print(f'Executing function to query index')
    try:
        index = GPTSimpleVectorIndex.load_from_disk(index_name)
        response = index.query(query)
        print(response)
        return True
    except Exception as e:
        print(f'Error querying the index: {e}')
        return False

"""
List of functions
"""
#list_buckets()
#get_bucket(bucket_name)
#list_blobs(bucket_name)
#download_blob(bucket_name,file_name_bucket,file_name_local)
#create_index(directory,index_name)
upload_index_to_bucket(index_name_bucket, file_name_local, bucket_name)
#query_index(index_name,query)

