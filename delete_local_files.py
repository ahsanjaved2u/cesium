import os
import shutil

def delete_files_in_folder(folder_path):
    try:
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path) 
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path) 
            print(f"Files in {folder_path} deleted successfully.")
        else:
            print(f"Folder {folder_path} does not exist.")
    except Exception as e:
        print(f"Error deleting files in {folder_path}: {e}")

def call_delete_files_in_folder():
    delete_files_in_folder('downloads')
    delete_files_in_folder('uploads')

# call_delete_files_in_folder()