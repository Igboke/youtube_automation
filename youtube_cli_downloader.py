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
