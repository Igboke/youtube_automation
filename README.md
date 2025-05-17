# YouTube CLI Downloader

A command-line tool to download YouTube videos or audio directly to your computer. You can specify video quality for progressive or adaptive MP4 streams or choose to download audio only.

## Features

* Download YouTube videos.
* Download audio-only from YouTube videos (highest available quality MP4 audio, falls back to other formats if MP4 audio not found).
* List available progressive MP4 video qualities for a given URL.
* Select a specific progressive MP4 video quality for download (e.g., "720p", "360p").
* Specify an output directory for downloads.
* Displays download progress.

## Prerequisites

* Python 3.6+
* `pip` (Python package installer)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Igboke/youtube_automation.git
    cd youtube_automation
    ```

    Or, simply download the `youtube_cli_downloader.py` script to a directory.

2. **Install dependencies:**
    Navigate to the directory containing the script and run:

    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional) Make the script executable (Linux/macOS):**

    ```bash
    chmod +x youtube_cli_downloader.py
    ```

## Usage

The basic command structure is:

```bash
python youtube_cli_downloader.py  [OPTIONS] <YOUTUBE_URL>
```

Or, if made executable (Linux/macOS):

```bash
./youtube_cli_downloader.py  [OPTIONS] <YOUTUBE_URL>
```

**Arguments:**

* `url`: (Required) The full URL of the YouTube video.

**Options:**

* `-h, --help`: Show the help message and exit.
* `-o OUTPUT, --output OUTPUT`:
    Specify the directory where the downloaded file should be saved.
    Defaults to the current directory (`.`).
* `-a, --audio`:
    Download audio only. The best available MP4 audio stream will be chosen.
    If specified, the `-q` / `--quality` option is ignored.
* `-q QUALITY, --quality QUALITY`:
    Specify the desired video quality for progressive MP4 streams (e.g., "720p", "480p", "360p", "240p", "144p").
    If the specified quality is not found as a progressive MP4 stream, the script will attempt to download the highest available progressive MP4 stream.
    This option is ignored if `-a` / `--audio` is used.
* `-l, --list-qualities`:
    List all available progressive MP4 video qualities (resolution, FPS, approximate size) for the given URL and then exit.
    No download will occur if this flag is used.

### Examples

1. **Download a video in the highest available progressive MP4 quality to the current directory:**

    ```bash
    python youtube_cli_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
    ```

2. **List available progressive MP4 qualities for a video:**

    ```bash
    python youtube_cli_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -l
    ```

    Output might look like:

    ```txt
    Processing URL: https://www.youtube.com/watch?v=VIDEO_ID
    Video Title (Initial Check): Example Video Title

    Available progressive MP4 qualities for 'Example Video Title':
      1. Resolution: 720p, FPS: 30, Size: 50.25MB (approx)
      2. Resolution: 480p, FPS: 30, Size: 25.10MB (approx)
      3. Resolution: 360p, FPS: 30, Size: 10.50MB (approx)
    ```

3. **Download a video in "360p" quality to a specific folder named `my_videos`:**

    ```bash
    python youtube_cli_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 360p -o ./my_videos
    ```

4. **Download audio only to a folder named `my_music`:**

    ```bash
    python youtube_cli_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -a --output ./my_music
    ```

## Notes

* This tool downloads progressive streams (video and audio combined in one file) for simplicity. Very high resolutions (1080p60, 1440p, 4K) on YouTube are often served as adaptive streams (separate video and audio files), which would require an additional tool like FFmpeg to merge. This script currently does not handle merging adaptive streams. But it download adaptive streams where there are no progressive streams
* Video availability and downloadable formats are determined by YouTube and can change.
* Ensure you have the necessary permissions to download content and respect YouTube's Terms of Service and copyright laws.

## Troubleshooting

* **"Error: Video ... is unavailable"**: The video might be private, deleted, region-locked, or have other restrictions.
* **"No progressive MP4 streams found"**: The video might not offer combined video/audio MP4 streams, or they might be in formats not currently filtered for.
* **Outdated `pytubefix`**: YouTube frequently updates its site. If downloads stop working, try updating the `pytubefix` library:

    ```bash
    pip install --upgrade pytubefix
    ```

## Disclaimer

This script is for educational purposes. Please respect copyright laws and YouTube's Terms of Service when downloading content. The developers of this script are not responsible for its misuse.
