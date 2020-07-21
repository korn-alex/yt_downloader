import subprocess
import re
from pprint import pprint
import datetime
import os
from toolbox.web import Downloader
from yt_downloader import zip_extractor
from yt_downloader import Tracklist
from pathlib import Path

def convert(video: str=None, extension: str='mp3', out_name:str=None, out_duration=None, additional_params:list=[]):
    """ converts a video(path) into mp3 """
    # check_ffmpeg()
    # d = ffmpeg.probe(video)
    video_path = Path(video)
    # video = video.replace('\\','')
    if out_duration:
        duration = out_duration
    else:   
        duration = get_duration(video_path)
    # try:
    #     duration = float(d['format']['duration'])
    # except Exception as identifier:
    #     print('reading duration failed')
    #     duration = 1
    # adding -vn to make it ignore video output
    # pix_fmt for whatsapp videos, libx264 ist der h264 codec
    # cmd = fr'ffmpeg -i "{video}" {additional_params} -c:v libx264 -pix_fmt yuv420p -aq 4 -y "{video_name}.{extension}"'
    if out_name:
        output_name = out_name
    else:
        output_name = video_path.stem
    cmd = ['ffmpeg',
            '-i', f'{video_path}', # file
            ]
    if not extension:
        extension = 'mp3'
    cmd += additional_params
    # out_dir = os.path.dirname(video)
    out_dir = video_path.parent
    cmd += [
            # '-c:a','libmp3lame',
            '-movflags', 'faststart',
            '-pix_fmt', 'yuv420p', # for whatsapp
            # '-c:v', 'libx264', # h264 codec 
            # '-profile:v', 'baseline',
            # '-level', '3.0',
            # '-c:a', 'aac',
            '-vf', "scale=trunc(iw/2)*2:trunc(ih/2)*2", # changes size, needs to be divisible by 2
            '-crf', '19', # quality (19-24) 19=best
            # '-threads', '0',
            # '-ab', '320k',
            # '-aq', '4', # audio quality
            ]
    cmd += ['-y', f'{out_dir}/{output_name}.{extension}'] # output file
    # cmd += ['-y', f'{video_path.name}.{extension}'] # output file
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    pattern = re.compile(r'time=[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9]')
    start_time = datetime.datetime.now()
    print(process.stderr)
    for line in process.stdout:
        if 'time=' in line:
            start = line.find('time=')
            time = line[start:].split(' ')[0]
            time = line.split('=')[1]
        #print(line)
        time_string = re.findall(pattern,line)
        if time_string:
            time = time_string[0].split('=')[1]
            hour, minute, second = time.split(':')
            time_in_sec = int(hour)*3600 + int(minute)*60 + float(second)
            #print(f'Hours:{hour}, Minutes:{minute}, Seconds:{second}, Time in seconds:{time_in_sec}')
            try:
                percent = time_in_sec / duration * 100
                print( f'Converting "{out_dir}/{output_name}.{extension}" {percent:.2f}%',end='\r' )
            except:
                print( f'Converting "{output_name}"...',end='\r' )
    end_time = datetime.datetime.now() - start_time
    print(f'\nDone in: {end_time}')
                

def get_duration(video):
    cmd = ['ffprobe', '-i', f'{video}']
    ffprobe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    pattern = re.compile(r'(?<=Duration:.)[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9]')
    duration = 0
    # parsing through output to find the duration string
    for line in ffprobe.stdout:
        # print(line)
        if 'Duration' in line:
            duration = pattern.findall(line)
            break
    try:
        hour, minute, second = duration[0].split(':')
        time_in_sec = int(hour)*3600 + int(minute)*60 + float(second)
        duration = time_in_sec
    except:
        duration = None
    return duration
    
def audio_boost(video: str=None, extension: str='mp3'):
    """ boosts low audio """
    check_ffmpeg()
    cmd = ["ffmpeg.exe", "-i", f"{video}", "-af", "volumedetect", "-vn", "-sn", "-dn", "-f", "null", "NUL"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
    pattern = re.compile(r'(?<=max_volume:.[-])\d+[.]?\d+')
    for line in process.stdout:
        #print(line)
        maxvol_string = re.findall(pattern,line)
        if maxvol_string:
            print(maxvol_string)
            convert(video, extension, fr'-af "volume={maxvol_string[0]}dB"')

def check_ffmpeg():
    _CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]
    _FFMPEG_URL = 'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20180829-d71dfc0-win64-static.zip'
    ffmpeg_set = {'ffmpeg.exe','ffprobe.exe'}
    files_set = set(os.listdir())
    if not ffmpeg_set.issubset(files_set):
        print('ffmpeg not found, downloading ffmpeg')
        d = Downloader()
        d.download(_FFMPEG_URL, _CURRENT_DIR)
        zip_extractor.extract(os.path.basename(_FFMPEG_URL), _CURRENT_DIR)

def split_mix(mix, clean_tracklist:list, fade_duration=3, out_ext=None):
    """
    takes in the list with dictionaries where trackname, timestamp and duration is found
    """
    mix_name, mix_ext = os.path.splitext(mix)
    if out_ext:
        mix_ext = out_ext
    for track in clean_tracklist:
        trackname = track['trackname']
        timestamp = track['timestamp']
        timestamp_seconds = track['timestamp_seconds']
        duration = track['duration']
        duration_stamp = track['duration_stamp']
        # -t starting time in 00:00:00 format
        # -ss start sample at 00:00:00 time
        # -af autofade in at total seconds and out at seconds+duration
        # d=fading duration
        split_file_additional_params = [
            '-t', f'{duration_stamp}',
            '-ss', f'{timestamp}',
            '-af', f'afade=t=in:st={timestamp_seconds}:d={fade_duration},afade=t=out:st={timestamp_seconds+duration-fade_duration}:d={fade_duration}',
        ]
        convert(mix,
                extension=mix_ext,
                out_name=trackname,
                out_duration=duration,
                additional_params=split_file_additional_params
                )


if __name__ == '__main__':
    _CURRENT_DIR = os.path.split(os.path.abspath(__file__))[0]
    def main_loop_convert():
        print('General Converter')
        while True:
            ext = input('Output extension. Enter for mp3): ')
            file = input('Drop file or folder with files here: ')
            file = file.replace('"','')
            if os.path.isdir(file):
                print('its a dir')
                dirs = os.listdir(file)
                # filter only files
                files = [os.path.join(file,f) for f in dirs if os.path.isfile(os.path.join(file,f))]
                print(files)
                for f in files:
                    convert(f,ext)
            else:
                print('its a file')
                print(file)
                convert(file,ext)
    
    def main_loop_audioboost():
        while True:
            ext = input('Output extension. Enter for mp3): ')
            file = input('Drop file or folder with files here: ')
            file = file.replace('"','')
            if os.path.isdir(file):
                print('its a dir')
                dirs = os.listdir(file)
                # filter only files
                files = [os.path.join(file,f) for f in dirs if os.path.isfile(os.path.join(file,f))]
                print(files)
                for f in files:
                    audio_boost(f,ext)
            else:
                print('its a file')
                print(file)
                audio_boost(file,ext)
    
    def auto_playlist_split(track_file_path:str, video_path:str):
        with open(track_file_path, 'r') as f:
            desc = f.read()
        lst = Tracklist.make_tracklist(desc, 5916)
        split_mix(video, lst, out_ext='mp3')
    
    def test(video_path:str):
        print(get_duration(video_path))

    main_loop_convert()
    # main_loop_audioboost()
    # auto_playlist_split()
    # test()