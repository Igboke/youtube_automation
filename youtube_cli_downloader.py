import argparse
import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError

def list_available_qualities(yt):
    """
    List the available video qualities for a YouTube video.
    """
    print(f"Avalaible video qualities for {yt.title}: \n")
    streams = yt.streams.filter(progressive=True,file_extension="mp4").order_by("resolution").desc()

    if not streams:
        print("No available Stream found.")
        return False
    
    for i, stream in enumerate(streams):
        size_mb = stream.filesize/(1024*1024) if stream.filesize else "N/A"
        print(f"{i+1}. Resolution: {stream.resolution}, FPS: {getattr(stream,"fps","N/A")}, Size: {size_mb:.2f} MB")
        return True
    
def on_progress(stream,chunk,bytes_remaining):
    """
    Callback function to show download progress.
    """
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded/total_size * 100
    print(f"Downloaded {bytes_downloaded//1024}KB of {total_size//1024}KB ({percentage:.2f}%)", end="\r")

def on_complete(stream,file_path):
    """
    Callback function to show download completion.
    """
    print(f"Download completed! File saved to {file_path}")

def download_video_cli(video_url,output_path=".",audio_only=False,quality=None,list_qualities=False):
    """
    Download a youtube video or audio from the given URL with quality selection.
    """
    try:
        print(f"Downloading video from {video_url}...")
        yt = YouTube(
            video_url,
            on_progress_callback=on_progress,
            on_complete_callback=on_complete
        )
        
    except VideoUnavailable:
        print("Video is unavailable.")
