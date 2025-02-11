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
    """Ensure that our necessary directories exist."""
    for d in [CONFIG['input_dir'], CONFIG['output_dir'], CONFIG['download_dir']]:
        Path(d).mkdir(exist_ok=True)

def download_video():
    """Download a YouTube video in the specified format."""
    url = input("Enter YouTube URL: ")
    
    # Get available formats
    subprocess.run(f"yt-dlp -F {url}", shell=True)
    
    format_choice = input(
        f"Enter format code [default {CONFIG['default_quality']}] (you can add + if you want multiple): "
    ) or CONFIG['default_quality']
    
    # Download the video based on chosen format
    subprocess.run(
        f"yt-dlp -f {format_choice} "
        f"-o '{CONFIG['download_dir']}/%(title)s.%(ext)s' {url}",
        shell=True
    )

def download_mp3():
    """Download a YouTube video as an MP3 file."""
    url = input("Enter YouTube URL: ")
    
    # Get available formats
    subprocess.run(f"yt-dlp -F {url}", shell=True)
    
    format_choice = CONFIG['default_quality']
    
    # Download and extract audio to MP3
    subprocess.run(
        f"yt-dlp -f {format_choice} --extract-audio --audio-format mp3 "
        f"-o '{CONFIG['download_dir']}/%(title)s.%(ext)s' {url}",
        shell=True
    )

def process_videos():
    """
    List the videos in the 'downloads' folder,
    allow user to pick one, then crop it using ffmpeg
    according to the input start and end times.
    """
    files = os.listdir(CONFIG['download_dir'])
    if not files:
        print("No files found in downloads folder to process.")
        return

    print("\nFiles in downloads folder:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f}")
    
    choice = input("\nSelect a file number to crop: ")
    try:
        choice_index = int(choice) - 1
        if choice_index < 0 or choice_index >= len(files):
            print("Invalid file selection.")
            return
    except ValueError:
        print("Invalid input.")
        return
    
    selected_file = files[choice_index]
    input_path = os.path.join(CONFIG['download_dir'], selected_file)
    
    # Ask user for the start time and end time
    start_time = input("Enter start time in HH:MM:SS (e.g., 00:01:30): ")
    end_time   = input("Enter end time in HH:MM:SS (e.g., 00:02:45): ")
    
    # Build the output file name
    base_name, ext = os.path.splitext(selected_file)
    cropped_filename = f"{base_name}_cropped{ext}"
    output_path = os.path.join(CONFIG['output_dir'], cropped_filename)
    
    # Run ffmpeg to crop the video
    # -ss sets the start time, -to sets the end time,
    # -c copy tries to copy without re-encoding (faster and no quality loss if the format supports it).
    command = (
        f'ffmpeg -i "{input_path}" '
        f'-ss {start_time} -to {end_time} '
        f'-c copy "{output_path}"'
    )
    print(f"\nRunning command:\n{command}\n")
    
    subprocess.run(command, shell=True)
    print(f"Crop complete! Cropped video saved as: {output_path}")

def main():
    ensure_dirs()
    while True:
        action = input(
            "\nMain Menu:\n"
            "1. Download mp3\n"
            "2. Download Video\n"
            "3. Process (Crop) Videos\n"
            "4. Exit\n> "
        )
        
        if action == '1':
            download_mp3()
        elif action == '2':
            download_video()
        elif action == '3':
            process_videos()
        elif action == '4':
            print("Exiting script.")
            break
        else:
            print("Invalid selection. Please choose a valid number.")

if __name__ == "__main__":
    main()
