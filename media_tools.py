import subprocess
import os
from pathlib import Path
import logging
import re

logging.basicConfig(level=logging.INFO, filename="media_tool.log")

CONFIG = {
    'input_dir': 'input',
    'output_dir': 'processed',
    'download_dir': 'downloads',
    'default_quality': '140'
}

def ensure_dirs():
    for d in CONFIG.values():
        Path(d).mkdir(parents=True, exist_ok=True)

def validate_youtube_url(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\\.)?'
        '(youtube|youtu|youtube-nocookie)\\.(com|be)/'
        '((watch\\?.*v=)|embed/|v/)?([\\w-]+)'
    )
    return youtube_regex.match(url) is not None

def download_video(url, format_choice=None):
    if not validate_youtube_url(url):
        logging.error("Invalid URL provided for video download.")
        return False

    format_choice = format_choice or CONFIG['default_quality']
    command = [
        "yt-dlp", "-f", format_choice,
        "-o", os.path.join(CONFIG['download_dir'], "%(title)s.%(ext)s"), url
    ]

    try:
        subprocess.run(command, check=True)
        logging.info(f"Video downloaded successfully from {url}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed downloading video: {e}")
        return False

def download_mp3(url):
    if not validate_youtube_url(url):
        logging.error("Invalid URL provided for MP3 download.")
        return False

    command = [
        "yt-dlp",
        "-f", CONFIG['default_quality'],
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", os.path.join(CONFIG['download_dir'], "%(title)s.%(ext)s"),
        url
    ]

    try:
        subprocess.run(command, check=True)
        logging.info(f"MP3 downloaded successfully from {url}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed downloading MP3: {e}")
        return False

def process_video(input_filename, start_time, end_time):
    input_path = os.path.join(CONFIG['input_dir'], input_filename)
    base_name, ext = os.path.splitext(input_filename)
    cropped_filename = f"{base_name}_cropped{ext}"
    output_path = os.path.join(CONFIG['output_dir'], cropped_filename)

    command = [
        "ffmpeg", "-i", input_path,
        "-ss", start_time, "-to", end_time,
        "-c:v", "copy", "-c:a", "copy",
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        logging.info(f"Cropped video saved as: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error cropping video: {e}")
        return False

def list_video_files():
    video_extensions = (".mov", ".mp4", ".avi", ".mkv", ".wmv", ".flv", ".webm")
    return [
        f for f in os.listdir(CONFIG['input_dir'])
        if f.lower().endswith(video_extensions)
    ]

def main():
    ensure_dirs()
    while True:
        action = input(
            "\nMain Menu:\n"
            "1. Download MP3\n"
            "2. Download Video\n"
            "3. Crop Any Video\n"
            "4. Exit\n> "
        )

        if action == '1':
            url = input("Enter YouTube URL: ")
            download_mp3(url)
        elif action == '2':
            url = input("Enter YouTube URL: ")
            format_choice = input(f"Enter format [default {CONFIG['default_quality']}]: ") or CONFIG['default_quality']
            download_video(url, format_choice)
        elif action == '3':
            files = list_video_files()
            if not files:
                print("No video files found. Inside the input folder.")
                continue

            for idx, file in enumerate(files, 1):
                print(f"{idx}. {file}")

            file_choice = int(input("Select file number: ")) - 1
            if 0 <= file_choice < len(files):
                start_time = input("Enter start time (HH:MM:SS): ")
                end_time = input("Enter end time (HH:MM:SS): ")
                process_video(files[file_choice], start_time, end_time)
            else:
                print("Invalid selection.")
        elif action == '4':
            print("Exiting.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()