import subprocess
import os
from pathlib import Path

CONFIG = {
    'input_dir': 'input',
    'output_dir': 'processed',
    'download_dir': 'downloads',
    'default_quality': '140'
}

def ensure_dirs():
    for d in [CONFIG['input_dir'], CONFIG['output_dir'], CONFIG['download_dir']]:
        Path(d).mkdir(exist_ok=True)

def download_video():
    url = input("Enter YouTube URL: ")
    # Get available formats
    subprocess.run(f"yt-dlp -F {url}", shell=True)
    format_choice =input(f"Enter format code [default {CONFIG['default_quality']}] + to add values: ") or CONFIG['default_quality']
    
    subprocess.run(
        f"yt-dlp -f {format_choice}"
        f"-o '{CONFIG['download_dir']}/%(title)s.%(ext)s' {url}",
        shell=True
    )
def download_mp3():
    url = input("Enter YouTube URL: ")
    # Get available formats
    subprocess.run(f"yt-dlp -F {url}", shell=True)
    format_choice =CONFIG['default_quality']
    
    subprocess.run(
        f"yt-dlp -f {format_choice} --extract-audio --audio-format mp3 "
        f"-o '{CONFIG['download_dir']}/%(title)s.%(ext)s' {url}",
        shell=True
    )

def main():
    ensure_dirs()
    while True:
        action = input("\nMain Menu:\n1. Download mp3 \n2. Download Video\n3. Process Videos\n4. Exit\n> ")
        if action == '1':
            download_mp3()
        if action == '2':
            download_video()
        elif action == '3':
            process_videos()
        elif action == '3':
            break

if __name__ == "__main__":
    main()