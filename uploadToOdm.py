import os
import requests
from flask import Flask, request, jsonify
import os
import json
import time


app = Flask(__name__)

status_codes = {
    'COMPLETED': 'COMPLETED',
    'FAILED': 'FAILED',
    'PROCESSING': 'PROCESSING'
}

# @app.route('/upload', methods=['POST'])
def upload_image(user_name, password, project_name, image_files):
    print(request.files)
    res = requests.post('http://localhost:8000/api/token-auth/', 
                        data={'username': user_name,
                              'password': password}).json()

    token = res.get('token')
    if not token:
        return jsonify({'error': 'Authentication failed'}), 401

    res = requests.post('http://localhost:8000/api/projects/', 
                        headers={'Authorization': 'JWT {}'.format(token)},
                        data={'name': project_name}).json()
    project_id = res.get('id')
    if not project_id:
        return jsonify({'error': 'Project creation failed'}), 400

    # Check the project creation response
    print("Project creation response:", res)

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

  
    # image_files = request.files.getlist('images')
    files = image_files
    images = []

    for file in files:
        image_path = os.path.join('uploads', file.filename)
        file.save(image_path)
        images.append(('images', (file.filename, open(image_path, 'rb'), file.mimetype)))

    options = json.dumps([
    {'name': "orthophoto-resolution", 'value': 24}
    ])

    # Create a task using the project_id and images
    try:
        task_creation_response = requests.post(
            'http://localhost:8000/api/projects/{}/tasks/'.format(project_id),
            headers={'Authorization': 'JWT {}'.format(token)},
            files=images,
            data={'options': options}
        ).json()
        print('task creation response is', task_creation_response)

        if 'id' in task_creation_response:
            task_id = task_creation_response.get('id')
        else:
            return jsonify({'error': 'Task creation failed', 'details': task_creation_response}), 400

        print("Task creation response:", task_creation_response)
    except Exception as e: 
        print(f'something went wrong: {e}')
    
  

    while True:
        res = requests.get('http://localhost:8000/api/projects/{}/tasks/{}/'.format(project_id, task_id), 
                           headers={'Authorization': 'JWT {}'.format(token)}).json()

        print("Response received:", res)

        if 'running_progress' in res:
            if res['running_progress'] == 1:
                print("Task has completed!")
                break
            # elif res['status'] == status_codes['FAILED']:
            #     print("Task failed: {}".format(res))
            #     sys.exit(1)
            else:
                print("Processing, hold on...")
        else:
            print("Unexpected response structure:", res)
            break

        time.sleep(3)

    return jsonify({"messages": res, "projectId": project_id, "task_id": task_id}), 200




# if __name__ == '__main__':
#     app.run(debug=True)

















































# @app.route('/upload', methods = ['POST'])
# def upload_image():

#     res = requests.post('http://localhost:8000/api/token-auth/', 
#                 data={'username': 'ahsanjaved161@yahoo.com',
#                         'password': 'Pakistan@123456'}).json()

#     token = res['token']
#     res = requests.post('http://localhost:8000/api/projects/', 
#                     headers={'Authorization': 'JWT {}'.format(token)},
#                     data={'name': 'My project'}).json()
#     project_id = res['id']

   

#     if not os.path.exists('uploads'):
#         os.makedirs('uploads')

    
#     if 'images' not in request.files:
#         return jsonify({'error': 'No images in request'}), 400
    
#     files = request.files.getlist('images')
#     image_paths = []
#     images = []
#     for file in files:
#         image_path = os.path.join('uploads', file.filename)
#         file.save(image_path)
#         image_paths.append(image_path)
#         images.append(('images', (file.filename, open(image_path, 'rb'), file.mimetype)))

#     options = json.dumps([
#     {'name': "orthophoto-resolution", 'value': 24}
#     ])
    

#     task_id = res['id']

#     # while True:
#     #     res = requests.get('http://localhost:8000/api/projects/{}/tasks/{}/'.format(project_id, task_id), 
#     #                 headers={'Authorization': 'JWT {}'.format(token)}).json()

#     #     if res['status'] == status_codes.COMPLETED:
#     #         print("Task has completed!")
#     #         break
#     #     elif res['status'] == status_codes.FAILED:
#     #         print("Task failed: {}".format(res))
#     #         sys.exit(1)
#     #     else:
#     #         print("Processing, hold on...")
#     #         time.sleep(3)


#     # return jsonify({"messags": res, "projectId": project_id, "task_id":task_id}), 200
    
    
#     res = requests.get('http://localhost:8000/api/projects/{}/tasks/{}/'.format(project_id, task_id), 
#                         headers={'Authorization': 'JWT {}'.format(token)}).json()   
 
#     print(res)
#     return jsonify({"messags": res, "projectId": project_id, "task_id":task_id, 'response':res}), 200
    
# if __name__=='__main__':
#     app.run(debug=True)