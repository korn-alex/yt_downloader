# from yt_downloader.txt_reader import read
from argparse import ArgumentParser
from yt_downloader import yt_downer
import json

# TODO keep original file option
# TODO make new directory for files option
parser = ArgumentParser()
parser.add_argument('-url', help='Youtube URL to download.')
parser.add_argument('-i','--input-file', help="Read URL's from a text file", type=str)
parser.add_argument('-f', '--format', help='Video or audio format to convert like: mp4. Default is mp3', type=str)
parser.add_argument('-dir', '--directory', help='Download directory', type=str)
parser.add_argument('-d', '--fade', help='Fade-in and fade-out in seconds between the tracks.', type=float)
parser.add_argument('-t', '--tracklist-in-description', help='If tracklist is in description', action='store_true')
parser.add_argument('-s', '--stamps', help='Make stamps: -s "name","3:44","3:50", "name2","3:50","3:53", ... Use only at the end.', nargs='*', type=str)
args = parser.parse_args()
# print(args.stamps)
# print(args)
yt_downer.main(args)