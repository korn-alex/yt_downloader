import zipfile
from os import path, remove
from pprint import pprint

def extract(in_path, out_path=None):
    """ extracts ffmpeg.exe ,ffprobe.exe and returns the path(str) to those directions """
    
    extract_files = ['ffmpeg.exe','ffprobe.exe']
    z = zipfile.ZipFile(in_path,'r')
    info = z.infolist()
    exe_list = []
    for i in info:
        for exe in extract_files:
            if exe in i.filename:
                exe_list.append(i.filename)
    name = z.namelist()
    #pprint(exe_list)
    for exe in exe_list:
        print(f'extracting {path.basename(exe)}')
        with open(path.basename(exe),'wb') as f:
            f.write(z.read(exe))
    z.close()
    print('removing zip')
    remove(in_path)
    #z.extractall(path=out_path, members=exe_list)
    print('extraction finished')
    #z.extract(exe_list[0])
    #z.printdir()