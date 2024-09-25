import requests
import os



# username = 'ahsanjaved161@yahoo.com'
# password = 'Pakistan@123456'
# project_id = '32' 
# task_id = 'a98233e9-51f3-4bd5-8aaa-0b109cdfb74e' 

def download_model(user_name, password, project_id, task_id):

    base_url = 'http://localhost:8000' 

    auth_url = f'{base_url}/api/token-auth/'
    auth_data = {'username': user_name, 'password': password}
    auth_response = requests.post(auth_url, data=auth_data)
    token = auth_response.json()['token']

    download_folder = 'downloads'


    # Set headers with the JWT token for subsequent requests
    headers = {'Authorization': f'JWT {token}'}

    #get available assets
    task_url = f'{base_url}/api/projects/{project_id}/tasks/{task_id}/'
    task_response = requests.get(task_url, headers=headers)

    if task_response.status_code == 200:
        task_data = task_response.json()
        print("Available Assets:", task_data['available_assets'])
    else:
        print(f"Error retrieving task information: {task_response.text}")
        exit()

    # Step 3: Define which assets to download (e.g., textured model and point cloud)
    assets_to_download = ['textured_model.zip', 'georeferenced_model.laz']

    #Ensure the 'downloads' folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for asset in assets_to_download:
        asset_url = f'http://localhost:8000/api/projects/{project_id}/tasks/{task_id}/download/{asset}'
        download_response = requests.get(asset_url, headers=headers, stream=True)

        if download_response.status_code == 200:
            file_name = asset
            file_path = os.path.join(download_folder, file_name)
            with open(file_path, 'wb') as file:
                for chunk in download_response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print(f"Downloaded: {file_name}")
            return download_response

        else:
            print(f"Failed to download {asset}: {download_response.status_code}")
