# Use official Python base image
FROM python:3.10.6-slim

# Set working directory inside container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
RUN pip install yt-dlp PyYAML

# Create necessary directories
RUN mkdir -p input processed downloads

# Define default command to run your script
CMD ["python", "media_tools.py"]

