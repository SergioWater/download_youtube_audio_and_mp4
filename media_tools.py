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
    format_choice = 137+140
    #input(f"Enter format code [default {CONFIG['default_quality']}]: ") or CONFIG['default_quality']
    
    subprocess.run(
        f"yt-dlp -f {format_choice} --merge-output-format mp4 "
        f"-o '{CONFIG['download_dir']}/%(title)s.%(ext)s' {url}",
        shell=True
    )

def process_videos():
    filters = {
        '1': {'name': 'Blurry', 'cmd': 'scale=iw:10'},
        '2': {'name': 'Vertical Strip', 'cmd': 'crop=iw:10:0:0'}
    }
    
    choice = input("Choose filter:\n1. Blurry Background\n2. Vertical Strip\n> ")
    
    for file in Path(CONFIG['input_dir']).iterdir():
        if file.suffix in ['.mp4', '.mov']:
            output_path = Path(CONFIG['output_dir']) / f"processed_{file.name}"
            # Add quotes around file paths to handle spaces
            cmd = f"ffmpeg -i \"{file}\" -vf \"{filters[choice]['cmd']}\" \"{output_path}\""
            subprocess.run(cmd, shell=True)
            print(f"Processed {file.name}")

def main():
    ensure_dirs()
    while True:
        action = input("\nMain Menu:\n1. Download Video\n2. Process Videos\n3. Exit\n> ")
        
        if action == '1':
            download_video()
        elif action == '2':
            process_videos()
        elif action == '3':
            break

if __name__ == "__main__":
    main()