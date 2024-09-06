from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    query = urlparse(url).query
    video_id = parse_qs(query).get("v")
    if video_id:
        return video_id[0]
    return None

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    query = urlparse(url).query
    video_id = parse_qs(query).get("v")
    if video_id:
        return video_id[0]
    return None

def download_transcript(video_url, output_file):
    video_id = get_video_id(video_url)
    if not video_id:
        print("Invalid YouTube URL.")
        return

    try:
        # Attempt to get the Chinese transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh', 'zh-TW'])
    except Exception as e:
        print(f"Chinese transcript not found. Trying to download English transcript. Error: {e}")
        try:
            # If Chinese transcript is not available, get the English transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except Exception as e:
            print(f"An error occurred while trying to download the English transcript: {e}")
            return

    with open(output_file, "w", encoding="utf-8") as file:
        for entry in transcript:
            file.write(f"{entry['text']} ({entry['start']}s)\n")
    print(f"Transcript saved to {output_file}")



if __name__=="__main__":
    # Replace this URL with your desired YouTube video URL
    youtube_url = "https://www.youtube.com/watch?v=3w7cyt2_dnI"
    output_file = "transcript.txt"
    download_transcript(youtube_url, output_file)
