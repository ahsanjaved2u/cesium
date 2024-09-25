import boto3
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import urllib.parse

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
cesium_access_token = os.getenv('cesium_access_token')

s3 = boto3.client(
    's3',
    region_name='ap-south-1',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
bucket_name = 'webodm-001'
s3_key = 'textured_model.zip'

# Step 1: Generate a pre-signed URL for the model file in S3
def generate_presigned_url(bucket_name, s3_key, expiration=3600):
    try:
        url = s3.generate_presigned_url('get_object',
                                         Params={'Bucket': bucket_name, 'Key': s3_key},
                                         ExpiresIn=expiration)
        return url
    except Exception as e:
        print(f"Error generating pre-signed URL: {str(e)}")
        return None

presigned_url = generate_presigned_url(bucket_name, s3_key)



# Asset details
assets = [
    {"key": "georeferenced_model.laz", "type": "POINT_CLOUD"},
    {"key": "textured_model.zip", "type": "3DTILES"}
]
# Presigned UR not neededin actual cesium documentation

# Step 2: Create an asset in Cesium using the S3 pre-signed URL
def create_cesium_asset_from_s3(asset_name, description):
    url = 'https://api.cesium.com/v1/assets'
    
    headers = {
        'Authorization': f'Bearer {cesium_access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
    'name': asset_name,
    'description': description,
    'type': 'GLTF',
    "options": {
        "sourceType": "3D_MODEL"
        },
    
    'from': {
        'type': 'S3',
        'bucket': bucket_name,
        'credentials': {
            'accessKey': 'AKIAS74TMF2VG7NELG4D', 
            'secretAccessKey': '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',  
        },
        'keys': ['textured_model.zip'],
    }
    }

    print('cesium access token is',cesium_access_token )
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        response = response.json()
        print(f"Successfully created asset: {response}")
        return response
    else:
        print(f"Error creating Cesium asset: {response.status_code}, {response.content}")
        return None


# asset_name = f"Model from S3: {s3_key}"
# description = f"This is a {asset_name.lower()} uploaded from S3 using a pre-signed URL."
# create_cesium_asset_from_s3(asset_name, description)







# Main execution loop
# for asset in assets:
#     s3_key = asset["key"]
#     asset_type = asset["type"]
    
#     # Generate the pre-signed URL for your model in S3
#     presigned_url = generate_presigned_url(bucket_name, s3_key)
    
#     if presigned_url:
#         asset_name = f"Model from S3: {s3_key}"
#         description = f"This is a {asset_type.lower()} uploaded from S3 using a pre-signed URL."
        
#         # Create an asset in Cesium
#         create_cesium_asset_from_s3(presigned_url, cesium_access_token, asset_name, description, asset_type)



