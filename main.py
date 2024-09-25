from flask import Flask, request, jsonify
from uploadToOdm import upload_image
from downloadModel import download_model
from uploadToS3 import upload_to_s3
from uploadToCesiumFromS3 import create_cesium_asset_from_s3
from delete_local_files import call_delete_files_in_folder

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def make_3d():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    project_name = request.form.get('project_name')
    description = request.form.get('description')

    # Check if the request contains image files
    if 'images' not in request.files:
        return jsonify({'error': 'No images in request'}), 400

    image_files = request.files.getlist('images')

    # Upload images
    response, status_code = upload_image(user_name, password, project_name, image_files)

    # Check the status of the image upload
    if status_code == 200:
        project_id = response.json.get("projectId")
        task_id = response.json.get("task_id")
        print("Task ID and Project ID:", project_id, task_id)

        # Download the 3D model
        res = download_model(user_name, password, project_id, task_id)
        if res.status_code == 200:
            # Upload to S3
            s3_res = upload_to_s3()
            if s3_res == 'done':
                # Create a Cesium asset from the S3 upload
                cesium_res = create_cesium_asset_from_s3(asset_name=project_name, description=description)
                if cesium_res['assetMetadata']['name'] == project_name:
                    call_delete_files_in_folder()
                    return jsonify({"Created Asset": cesium_res['assetMetadata']['id']})
                else:
                    call_delete_files_in_folder()
                    return jsonify({'error': 'Failed to create Cesium asset'}), 500
            else:
                return jsonify({'error': 'Failed to upload to S3'}), 500
        else:
            return jsonify({'error': 'Failed to download the 3D model'}), 500
    else:
        return jsonify({'error': 'Failed to upload images'}), 500

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/upload', methods = ['POST'])
# def make_3d():
#     user_name = request.form.get('user_name')
#     password = request.form.get('password')
#     project_name=request.form.get('project_name')
#     description = request.form.get('description')

#     if 'images' not in request.files:
#         return jsonify({'error': 'No images in request'}), 400

#     image_files = request.files.getlist('images')

#     response, status_code = upload_image(user_name, password, project_name, image_files)

#     # Now, check the status code
#     if status_code == 200:
#         project_id = response.json.get("projectId")
#         task_id = response.json.get("task_id")
#         print("task id and project id is", project_id, task_id)
#         res = download_model(user_name, password, project_id, task_id)
#         print(res)
#         print(res.status_code)
#         res.status_code ==200; 
        
#         if res.status_code == 200:
#             res = upload_to_s3()
#             print(res)
#             if res == 'done':
#                 res = create_cesium_asset_from_s3(asset_name=project_name,  description=description)
#                 if res['assetMetadata']['name'] ==  f'Model from S3: {project_name}':
#                     call_delete_files_in_folder()
#                     return jsonify({"Created Asset" : res['assetMetadata']['id']})