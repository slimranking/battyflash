import json
import os
from shutil import copyfile

import pendulum

def load_json(directory, file_name='flash_data.json'):
    """
    Load flash JSON from <directory>/<file_name>

    If the file doesn't exist, return None
    """
    full_path = os.path.join(directory, file_name)
    
    if not os.path.exists(full_path):
        return None
    
    with open(full_path) as f:
        data = json.load(f)

    return data


def store_json(d, directory, file_name='flash_data.json', backup=True):
    """
    Store <d> at <directory>/<file_name> as json

    If <directory>/<file_name> and <backup>:
        Create backup of existing at json at <directory>/.backups/<current_timestamp>.json
    """
    full_path = os.path.join(directory, file_name)
    
    create_dir_if_not_exists(full_path)

    if os.path.exists(full_path) and backup:
        now = pendulum.now().to_iso8601_string()
        backup_path = os.path.join(directory, '.backups', now+'.json')
        create_dir_if_not_exists(backup_path)
        copyfile(full_path, backup_path)

    with open(full_path, 'w') as fp:
        json.dump(d, fp)


def create_dir_if_not_exists(path):
    """
    If the directory at <path> does not exist, create it empty
    """
    directory = os.path.dirname(path)
    # Do not try and create directory if path is just a filename
    if (not os.path.exists(directory)) and (directory != ''):
        os.makedirs(directory)


def empty_backups():
    """
    Empty backup directory of jsons
    date ranges
    """
    pass


def list_in_folder():
    """
    list all files in folder
    recursive functionality?
    """
    pass


