import youtube_dl
# from argparse import ArgumentParser
# import txt_reader
from yt_downloader import convert
from yt_downloader.txt_reader import read as read_file
import os
# import file_downloader
# import zip_extractor
from yt_downloader import Tracklist
# import pip
import subprocess
import sys
import json
from pathlib import Path


def progess_hook(hook):
	print(f'hook: {hook["status"]}')


_CURRENT_FILE = os.path.abspath(__file__)
_CURRENT_DIR = os.path.split(_CURRENT_FILE)[0]
_OPTIONS = {
		'format': 'best',
		'noplaylist':True,
		'progress_hooks': [progess_hook],
		'outtmpl': f'{_CURRENT_DIR}/%(title)s.%(ext)s'
		#'postprocessors': [{
		#    'key': 'FFmpegExtractAudio',
		#    'preferredcodec': 'mp3',
		#    'preferredquality': '192',
		#}],
	}

def main(args):
	update_ytdl()
	print('')
	if args.input_file:
		urls = read_file(args.input_file)
	elif args.url:
		url = args.url
	else:
		url = input_loop()
	# TODO make settings for default download directory
	if args.directory:
		directory = Path(args.directory)
		_OPTIONS['outtmpl'] = f'{directory}/%(title)s.%(ext)s'
	else:
		# directory = Path().cwd()
		pass
	if args.tracklist_in_description and args.stamps:
		print('Tracklist and stamps cannot be used together.')
		return
	if args.format:
		ext = args.format
	else:
		ext = 'mp3'
	if args.fade:
		fade = args.fade
	else:
		fade = 0.1
	if args.tracklist_in_description:
		print(args)
		download_mix(url, fade_duration=fade)
	elif args.stamps:
		if len(args.stamps) % 3 == 0:
			stamp_count = int(len(args.stamps) / 3)
			stamps = []
			start = 0
			end = 3
			for i in range(stamp_count):
				stamp = args.stamps[start:end]
				stamps.append(stamp)
				start = end
				end += 3
			download_with_stamps(url, stamps=stamps, fade_duration=fade, ext=ext)
		else:
			print('-s has not enough arguments')
			return
	else:
		print('no tracklist')
		if args.input_file:
			dicts = download_list(urls)
			for dic in dicts:
				video = make_video_path(dic)
				convert.convert(video, ext)
		else:
			dic = download([url])
			video = make_video_path(dic)
			convert.convert(video, ext)
		
def update_ytdl():
	print('\nupdating youtube-dl')
	subprocess.call([sys.executable, "-m", "pip", "install",'-U', 'youtube-dl'])


def download(url_list: list, options=_OPTIONS, 
			tracklist_in_description=False,
			convert_timestamps=None):
	"""
	downloads url into mp4 and returns dictionary['title'],dictionary['ext'] 
	
	if `tracklist_in_description=True` it returns `tracklist`
	and `tracklist_duration`
	"""
	dic = {}
	with youtube_dl.YoutubeDL(options) as ydl:
		result = ydl.extract_info(url_list[0], download=False)
		if tracklist_in_description:
			tracklist = Tracklist.make_tracklist(result['description'], int(result['duration']))
			dic['tracklist'] = tracklist
			dic['tracklist_duration'] = result['duration']
		if convert_timestamps:
			tracklist = Tracklist.make_tracklist_from_timestamps(convert_timestamps)
			dic['tracklist'] = tracklist
			dic['tracklist_duration'] = result['duration']

		#dic['title'] = result['title']
		#dic['ext'] = result['ext']
		print(result['description'])
		# with open('desc.txt','w') as f:
		#     f.write(result['description'])
		filename = ydl.prepare_filename(result)
		dic['title'], dic['ext'] = os.path.splitext(filename)
		# j = ydl._pps
		ydl.download(url_list)
		return dic

def download_list(urls:list, options=_OPTIONS, 
			tracklist_in_description=False,
			convert_timestamps=None):
	dicts = []
	for url in urls:
		dic = download([url], options=options, tracklist_in_description=tracklist_in_description, convert_timestamps=convert_timestamps)
		dicts.append(dic)
	return dicts

def input_loop():
	""" asks user to make url input, returns url string """
	print('url einfügen und enter zum download\n')
	url = ''
	while not url:
		url = input()
		url = url.strip()
	return url

def make_video_path(dic: dict):
	"""
	takes in a dictionary with `title` and `ext` keys
	and returns the video path
	"""
	name = dic['title']
	ext = dic['ext']
	vp = Path(f'{name}{ext}')
	# TODO
	# new_dir = vp.parent / vp.stem
	# if not new_dir.is_dir():
	# 	try:
	# 		# os.mkdir(name)
	# 		new_dir.mkdir()
	# 	except Exception as e:
	# 		print(e)
	# 		new_dir = vp.parent
	# new_vp = new_dir / vp.name
	return vp

def download_mix(url, tracklist_in_description=True, fade_duration=0.1, ext='mp3'):
	print('Fade duration: ', fade_duration)
	print('Download mix with tracklist.')
	dic = download([url], tracklist_in_description=tracklist_in_description)
	video = make_video_path(dic)
	convert.split_mix(video, 
	                    dic['tracklist'], 
	                    out_ext=ext,
	                    fade_duration=fade_duration)

def download_with_stamps(url, stamps, tracklist_in_description=False, fade_duration=0.1, ext='mp3', options=_OPTIONS):
	# single video with timestamps
	try:
		#print(stamps)
		for s in stamps:
			#print(s)
			#s = tuple(s)
			#print(s[0])
			_, _, _ = s
	except:
		print('Incorrect stamp format. Should be in the format \'[["name","1:34","1:40"], ...]\'')
		return
	print('Download video with timestamps')
	dic = download([url], convert_timestamps=stamps, options=options)
	video = make_video_path(dic)
	convert.split_mix(video, 
						dic['tracklist'], 
						out_ext=ext,
						fade_duration=fade_duration)


if __name__ == "__main__":
	main()