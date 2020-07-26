import re
import datetime
from secrets import token_hex


""" 
Handles tracklisting from youtube descriptions
"""

REGSTAMP = re.compile(r'(\d{1,2}:){1,2}\d{1,2}\.?\d*')

def get_tracklist(description:str) -> list:
    """
    returns a list with lines where a timestamp is found
    """
    desc = description.split('\n')
    # in case the first track has no time notation
    # if nr == 0 and stamp == '':
    #     stamp = f'00:00:00'
    # ???

    # \d = [0-9]
    # \d* = zero or more matches
    # 4:20
    # 14:20
    # 1:14:20
    # regstamp = re.compile(r'\d*:*\d{1,2}:\d\d')
    relevant_lines = []
    for line in desc:
        if REGSTAMP.search(line):
            relevant_lines.append(line)
    return relevant_lines

def get_timestamp(track:str) -> str:
    """
    find "00:00:00" timestamp in the track string and returns a timestamp "00:00:00"
    """
    
    # regstamp = re.compile(r'\d*:*\d{1,2}:\d\d')
    # regstamp = re.compile(r'(\d{1,2}:)?\d{1,2}:\d{1,2}\.?\d*')
    # regstamp = re.compile(r'(\d{1,2}:){1,2}\d{1,2}\.?\d*')
    try:
        # stamp = REGSTAMP.search(track)[0]
        stamp = REGSTAMP.search(track).group()
        if stamp:
            # checking for min, hour and filling missing numbers with zeros
            # making every timestamp the following format: 00:00:00
            try:
                hour, minute, second = stamp.split(':')
                stamp = f'{hour.zfill(2)}:{minute.zfill(2)}:{second.zfill(2)}'
            except:
                minute, second = stamp.split(':')
                stamp = f'00:{minute.zfill(2)}:{second.zfill(2)}'
    except:
        raise RuntimeError(f'No timestamp found in "{track}"')
    return stamp

def timestamp_to_seconds(timestamp:str) -> float:
    """
    returns int(seconds) from 00:00:00 timestamp
    """

    hour, min, sec = timestamp.split(':')
    return int(hour)*3600 + int(min)*60 + float(sec)

def seconds_to_timestamp(seconds:float) -> str:
    """
    returns amount of seconds with milliseconds from a timestamp
    """
    # sec = f'{seconds:.6f}'
    time_delta = datetime.datetime(100,1,1,0,0,0) + datetime.timedelta(0,seconds)
    return time_delta.strftime('%H:%M:%S.%f')


def get_clean_trackname(track:str, name=None) -> str:
    """
    Parses track string and returns trackname without timestamp in the name.
    
    `name`: str, default is None.
    Sets name for track.
    """
    if name:
        stampless_str = name
    else:
        try:
            stamp_str = REGSTAMP.search(track).group()
        # random name
        except AttributeError:
            raise AttributeError(f'No timestamp found in "{track}"')
        stamp_length = len(stamp_str)
        stamp_start = track.find(stamp_str)
        stamp_end = stamp_start + stamp_length
        stampless_str = track[:stamp_start] + track[stamp_end:]
    # re.findall(r'[A-Za-z0-9_\-(){}]')
    # for ch in [r'(',r')',r'[',r']',r'{',r'}',r'/']:
    #     if ch in stampless_str:
    #         stampless_str=stampless_str.replace(ch,'')
    # track = {'trackname':stampless_str, 'timestamp':stamp_str}
    _clean = ''.join(re.findall(r'[A-Za-z0-9ÄÖÜäöüß_(){}&\s\-]', stampless_str))
    _clean_start = re.sub('^[&(){}\s\.]*', '', _clean)
    _clean_end = re.sub('[&(){}\s\.]*$', '', _clean_start)
    if not _clean_end:
        trackname = token_hex(16)
    else:
        trackname = _clean_end
    return trackname


def get_track_durations(tracks:list, full_duration:int)->list:
    """
    takes in a list with all tracks and returns a list with dicionaries
    with the keys: 'duration' (in seconds) and 'duration_stamp' (formatted to a stamp)
    """

    durations = []
    for nr in range(len(tracks)):
        stamp = get_timestamp(tracks[nr])
        start = timestamp_to_seconds(stamp)
        try:
            end_stamp = get_timestamp(tracks[nr+1])
            end = timestamp_to_seconds(end_stamp)
        except IndexError:
            end = full_duration
        # calculating durations with datetime objects
        # dummy_date + duration_in_seconds
        # and reformat back to 00:00:00
        duration = end-start
        time_delta = datetime.datetime(100,1,1,0,0,0) + datetime.timedelta(0,duration)
        duration_stamp = time_delta.strftime('%H:%M:%S')
        durations.append({'duration':duration,'duration_stamp':duration_stamp})
    return durations


def make_tracklist(description:str, full_duration:int)->list:
    """
    takes in a string of the description where the tracks are found
    returns a list with dictionary consisting of trackname and duration
    """
    lst = get_tracklist(description)   
    durations = get_track_durations(lst, full_duration)
    # durations_stamps = get_track_durations_as_timestamps(lst, full_duration)
    tracklist = []
    for track, duration in zip(lst, durations):
        clean_trackname = get_clean_trackname(track)
        timestamp = get_timestamp(track)
        timestamp_seconds = timestamp_to_seconds(timestamp)
        tracklist.append( {'trackname':clean_trackname,
                            'timestamp':timestamp,
                            'timestamp_seconds':timestamp_seconds,
                            'duration':duration['duration'],
                            'duration_stamp':duration['duration_stamp']
                            } 
                        )
    return tracklist

def make_tracklist_from_timestamps(track_tuples:list)->list:
    """
    takes in a list with track_tuples (track_name, start_stamp, end_stamp)
    and returns a list with dicionaries 
    """
    # lst = get_tracklist(description)   
    # durations = get_track_durations(lst, full_duration)
    # durations_stamps = get_track_durations_as_timestamps(lst, full_duration)
    tracklist = []
    for track in track_tuples:
        name, start, end = track
        clean_trackname = name
        timestamp = get_timestamp(start)
        end_stamp = get_timestamp(end)
        timestamp_seconds = timestamp_to_seconds(timestamp)
        end_timestamp_seconds = timestamp_to_seconds(end_stamp)
        duration = end_timestamp_seconds - timestamp_seconds
        duration_stamp = seconds_to_timestamp(duration)
        tracklist.append( {'trackname':clean_trackname, # name of track
                            'timestamp':timestamp, # timestamp where track starts
                            'timestamp_seconds':timestamp_seconds, # seconds where it starts
                            'duration':duration, # duration of track in seconds
                            'duration_stamp':duration_stamp # duration of track as a timestamp
                            } 
                        )
    return tracklist

if __name__ == "__main__":
    # print(get_timestamps(desc))
    # get_timestamp(lst[1])
    # tracks = get_clean_tracklist(lst)
    a = datetime.datetime(100,1,1,0,3,26)
    # start 5:04, end 5:07
    parts = [('test', '5:04', '5:07'),]
    make_tracklist_from_timestamps(parts)
    print('')
    print(a)
    print('')