import argparse
import os
from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable, RegexMatchError

def list_available_qualities(yt):
    """Lists available progressive mp4 video qualities more robustly."""
    try:
        video_title = yt.title 
    except Exception as e:
        print(f"\n  Error (list_qualities): Could not retrieve video title. (Details: {e})")
        print("  This might be due to an invalid URL, network issues, or the video being unavailable/restricted.")
        return False

    print(f"\nAvailable progressive MP4 qualities for '{video_title}':")

    try:
        if not hasattr(yt, 'streams') or yt.streams is None: 
            print("  Error (list_qualities): Video streams data is not available for this video object.")
            return False

        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

        if not streams:
            print("  No progressive MP4 streams found for this video.")
            streams = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc()
            return False

        for i, stream in enumerate(streams):
            try:
                size_mb_str = "N/A"
                if stream.filesize:
                    size_mb = stream.filesize / (1024 * 1024)
                    size_mb_str = f"{size_mb:.2f}MB"
                
                fps_str = getattr(stream, 'fps', 'N/A')
                res_str = getattr(stream, 'resolution', 'N/A')

                print(f"  {i+1}. Resolution: {res_str}, FPS: {fps_str}, Size: {size_mb_str} (approx)")
            except Exception as stream_detail_error:
                print(f"  Could not retrieve details for one stream: {stream_detail_error}")
        return True

    except AttributeError as ae:
        print(f"  Error (list_qualities): A required attribute ('streams' or similar) was missing. (Details: {ae})")
        return False
    except Exception as e:
        print(f"  Error (list_qualities): Error accessing/filtering video streams: {e}")
        return False
    
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
        if list_qualities:
            list_available_qualities(yt)
            return True
        if audio_only:
            stream = yt.streams.filter(only_audio=True,file_extension="mp4").order_by("abr").desc().first()
            if not stream:
                stream = yt.streams.get_audio_only()
                print("No audio stream found using default.")
        else:
            progressive_streams = yt.streams.filter(progressive=True,file_extension="mp4")
            if not progressive_streams:
                print("No progressive streams found, falling back to adaptive streams.")
                adaptive_streams = yt.streams.filter(adaptive=True,file_extension="mp4")
                if not adaptive_streams:
                    print("No adaptive streams found.")
                    return False
            if quality and progressive_streams:
                stream = progressive_streams.filter(resolution=quality).first()
                if stream:
                    print(f"Selected quality: {quality}")
            elif quality and adaptive_streams:
                stream = adaptive_streams.filter(resolution=quality).first()
                if stream:
                    print(f"Selected quality: {quality}")
            else:
                print("No suitable stream found")
                print("Try using --list-qualities to see available progressive MP4 options.")
            return False
        
        print(f"Downloading: {stream.mime_type}, Resolution/ABR: {stream.resolution or stream.abr}, FPS: {getattr(stream, 'fps', 'N/A')}")

        if not os.path.exists(output_path):
            os.mkdir(output_path)
        stream.download(output_path=output_path)
        return True
    except RegexMatchError:
        print("Invalid URL format. Please check the URL and try again.")
        return False
    
    except VideoUnavailable:
        print("Video is unavailable.")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube videos from the command line.")

    

