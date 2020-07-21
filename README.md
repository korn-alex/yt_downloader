# yt_downloader
A cli tool for downloading/converting videos from youtube.

### requirements
- ffmpeg
- ffprobe
- python3.8

### Using

Downloading video from "youtube url" and converting it to mp4 format:
```sh
python run.py -url "youtube url" -f "mp4"
```

Downloading a video and converting a 6 seconds part to mp3:
```sh
python run.py -url "youtube url" -f "mp3" -s "small_audio_part","3:44","3:50"
```

### Installation
1. create virtual environment
    ```sh
    python -m venv .env
    ``` 
2. activate environment

    Linux:
    ```sh
    . .env/bin/activate
    ```
    Windows:
    ```ps
    .env/Scripts/activate.ps1
    ```

3. install dependencies
    ```sh
    pip install -r requirements.txt
    ```

### Options
option | description
------- | --------
-h, --help | Showing available options.
-url | Youtube URL to download.
-i, --input-file | Read URL's from a text file
-f, --format | Video or audio format to convert like: mp4. Default is mp3
-dir, --directory | Download directory.
-d, --fade | Fade-in and fade-out in seconds between the tracks.
-t, --tracklist-in-description | Parses tracklist with `"hh:mm:ss" - "name"` format from video and splits accordingly.
| -s, --stamps | Convert splits from time stamps. Use only at the end.|
|              | format: `[name], [start time], [end time], ...` |
|              | example: `-s "split_1","3:44","3:50", "split_2","3:50","3:53"` |
