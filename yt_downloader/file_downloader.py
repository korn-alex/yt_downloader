import os
from sys import stdout
import requests


def download(url, d_path, out_name=None, session=None):
    """ downloads from url """

    def get_bar(progress):
        """progress must be between 0 and 1\n 
        Returns the bar with current progress as a string """
        FULL_BLOCKLENGTH = 32
        fillblock = '█'

        blocks = int(progress / (1/FULL_BLOCKLENGTH))
        bar_start = '\r'+fillblock*blocks
        bar_end = (33 - len(bar_start))*'_'+'|'
        if progress > 1:
            progress = 1
        bar_percent = f' {progress*100:0.2f} % '
        text = bar_start+bar_end+bar_percent
        return text
    
    name = os.path.split(url)[1]
    if out_name:
        name = out_name
    file = os.path.join(d_path,name)    
    if session:
        r = session.get(url)
    else:
        r = requests.get(url)
    size = float(r.headers['content-length'])
    with open(file, 'wb') as fd:
        tmp = 0
        print(f'Downloding: {name}')
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fd.write(chunk)
                tmp += 1024
                bar = get_bar(tmp / size)
                stdout.write(
                    f'\r{bar} {tmp/1000000:0.2f} / {size/1000000:0.2f} MB'.format(tmp))
        print('')
        print('Done')


async def async_download(url, d_path, session=None):
    """ Downloads from url \n
    Must be awaited """

    def get_bar(progress):
        """progress must be between 0 and 1\n 
        Returns the bar with current progress as a string """
        FULL_BLOCKLENGTH = 32
        fillblock = '█'

        blocks = int(progress / (1/FULL_BLOCKLENGTH))
        bar_start = '\r'+fillblock*blocks
        bar_end = (33 - len(bar_start))*'_'+'|'
        if progress > 1:
            progress = 1
        bar_percent = f' {progress*100:0.2f} % '
        text = bar_start+bar_end+bar_percent
        return text
    name_index = len(os.path.split(d_path))
    name = os.path.split(d_path)[name_index-1]
    if session:
        r = session.get(url)
    else:
        r = requests.get(url)
    size = float(r.headers['content-length'])
    with open(d_path, 'wb') as fd:
        tmp = 0
        print(f'Downloding: {name}')
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fd.write(chunk)
                tmp += 1024
                bar = get_bar(tmp / size)
                stdout.write(
                    f'\r{bar} {tmp/1000000:0.2f} / {size/1000000:0.2f} MB'.format(tmp))
        print('')
        print('Done')