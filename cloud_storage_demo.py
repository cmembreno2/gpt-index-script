import os 
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

storage_client = storage.Client()

"""
Create a New Bucket
"""
bucket_name = 'test-bucket-dataset-cm'
bucket = storage_client.bucket(bucket_name)
bucket.location = 'US'
bucket = storage_client.create_bucket(bucket)

"""
Print created bucket details
"""
vars(bucket)

"""
Accessing to the created bucket
"""
my_bucket = storage_client.get_bucket(bucket_name)

"""
Upload Files to created Bucket
"""
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

file_path = 'data'
file_name = 'Copy of Copy of 2020 08 04 Copilot Intro demo for xpt.txt'
file_name_stored = 'kalepa-dataset/Copy of Copy of 2020 08 04 Copilot Intro demo for xpt.txt'
file_name_local= 'Copy of Copy of 2020 08 04 Copilot Intro demo for xpt.txt'
upload_to_bucket(file_name_stored, os.path.join(file_path, file_name), bucket_name)

"""
Download Files from created Bucket
"""
def download_blob(bucket_name, source_blob_name, destination_file_name):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print("Saved")
        return True
    except Exception as e:
        print(f'Not saved: {e}')
        return False
    
download_blob(bucket_name,file_name_stored,file_name_local)