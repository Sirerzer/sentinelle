import os
import time
import shutil

def is_file_being_uploaded(file_path):
    try:
        initial_size = os.path.getsize(file_path)
        time.sleep(0.1)
        final_size = os.path.getsize(file_path)
        return initial_size != final_size
    except:
        return True

def move_large_file(file_path, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    dest_path = os.path.join(destination_folder, os.path.basename(file_path))
    shutil.move(file_path, dest_path)
    return dest_path
