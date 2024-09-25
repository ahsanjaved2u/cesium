import boto3
import os
from dotenv import load_dotenv
load_dotenv()

def upload_to_s3():
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


    s3 = boto3.client('s3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    # Step 1: Set up S3 client
    bucket = 'webodm-001'
    folder_name = 'client-1_site-1'

    # if object_name is None:
    #     object_name = os.path.basename(file_name)


    # path to the file you want to upload
    folede_path = r'C:\Users\dell\Desktop\webODM\downloads'

    for file_name in os.listdir(folede_path):
        file_path = os.path.join(folede_path, file_name)
        object_name =file_name
        if os.path.isfile(file_path):  # Ensure it's a file
            try:
                response = s3.upload_file(file_path, bucket, object_name)
                print(f'Uploaded {file_name} to {bucket}/{folder_name}')
                return 'done'
            except Exception as e:
                print(f'Failed to upload {file_name}: {e}')

