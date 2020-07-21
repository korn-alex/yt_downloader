import os
import glob
from pathlib import Path


def read(path=None):
    """ reads the txt file and returns its urls as a list """ 
    if path is None:
        path = _get_own_file_path()
    # folder_path, cur_dir_file = os.path.split(path)
    file_path = Path(path)
    folder_path = file_path.parent
    print(f'TEXT FILE: {file_path}')
    url_lines = _open_file(file_path)
    return url_lines

def _get_own_file_path():
    return os.path.abspath(__file__)

def _create_txt(path):
    """ creates empty music.txt if it doesnt exist """
    try:
        with open(path,'w') as f:
            f.write('')
    except Exception as e:
        print(f'Something went wrong creating music.txt in {path}: {e}')

def _open_file(txt_file):
    """ opening the text file and returning its contents as list """
    url_lines = []
    try:
        with open(txt_file,'r') as fp:
            for line in fp.readlines():
                url_lines.append(line.strip())
    except Exception as e:
        print(f'exception when opening:{txt_file}',e)
        return
    return url_lines