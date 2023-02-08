# importing libraries
import sys
import os 
from google.cloud import storage
import os
import openai
from dotenv import load_dotenv
from gpt_index import GPTSimpleVectorIndex, Document
from gpt_index import (
    LLMPredictor
)
from langchain import OpenAI

# set up google client with credentials, open ai
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials/credentials.json'
storage_client = storage.Client()
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
 
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

# function to upload a blob to bucket
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
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
        # if bucket exists download the files from kalepa's folder
        if bucket_exists:
            files_download = []
            blobs_paths_bucket = []
            txt_files = []
            json_files = []
            txt_base_names = []
            json_base_names = []
            prefix = folder+'/'
            blobs = list_blobs(bucket_name, prefix)
            for blob in blobs:
                blobs_paths_bucket.append(blob.name)
            for blob in blobs_paths_bucket:
                # get the files with extension .txt
                extensionsToCheck = ['.txt']
                for extension in extensionsToCheck:
                    if extension in blob:
                        txt_files.append(blob)
                # get the files with extension .json
                extensionsToCheck = ['.json']
                for extension in extensionsToCheck:
                    if extension in blob:
                        json_files.append(blob)
            # prepare txt files to be compared with json files
            for file in txt_files:
                split_name = file.split('/')
                file_path = split_name[1]
                file_name = file_path.split('.')
                base_name = file_name[0]
                txt_base_names.append(base_name)
            # prepare json files to be compared with txt files
            for file in json_files:
                split_name = file.split('/')
                file_path = split_name[1]
                file_name = file_path.split('.')
                base_name = file_name[0]
                json_base_names.append(base_name)
            # verify the .txt files that need an index
            for file in txt_base_names:
                if file in json_base_names:
                    print(f'Index already in GCS for : {file}')
                else:
                    files_download.append(file)
            # download the .txt files that need an index
            for file in files_download:
                download_blob(bucket_name,blob,'data/'+file+'.txt')
            # for each downloaded file create an index.json file and save it in directory
            for filename in os.listdir('data/'):
                f = os.path.join('data/',filename)
                if os.path.isfile(f):
                    with open(f, encoding="utf-8") as file:
                        file_text = file.read().rstrip()
                        text_list = [file_text]
                        documents = [Document(t) for t in text_list]
                        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
                        index = GPTSimpleVectorIndex(documents,llm_predictor=llm_predictor)
                        file_name = f
                        split_name = file_name.split('/')
                        file_name = split_name[1]
                        split_index_name = file_name.split('.')
                        index_name = split_index_name[0]
                        index.save_to_disk(f'indexes/{index_name}.index.json')
            for filename in os.listdir('indexes/'):
                f = os.path.join('indexes/',filename)
                if os.path.isfile(f):
                    file_name = f
                    split_name = file_name.split('/')
                    file_name = split_name[1]
                    blob_name = folder+'/'+file_name
                    print('Uploading documents')
                    upload_to_bucket(blob_name, f, bucket_name)
                    print('Indexes uploaded to bucket')
        # if bucket does not exist print a message and finish process
        else:
            print('Bucket does not exist in project, end of process')
    except Exception as e:
        print(f'Error executing main: {e}')   

if __name__ == "__main__":
    main_script(sys.argv[1],sys.argv[2])