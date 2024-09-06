from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp
import yt_dlp
import os
from datetime import datetime
from pydub import AudioSegment
from typing import List

def seconds_to_hms(secs):
    # Extract hours, minutes, seconds
    hours = int(secs // 3600)
    minutes = int((secs % 3600) // 60)
    seconds = secs % 60
    
    # Format the result with milliseconds
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:06.3f}"
    return formatted_time


def audio_to_transcript(video_path):
# checkpoint="openai/whisper-large-v2",
# dtype=jnp.float32,
# batch_size=None,
# max_length=None,
    pipeline = FlaxWhisperPipline(checkpoint="openai/whisper-medium",
                                dtype=jnp.float32,
                                batch_size = 1)



    text = pipeline(video_path, task="transcribe", return_timestamps=True)

    with open('./transcript.txt', 'w', encoding='utf-8') as f:
        for line in text['chunks']:
            f.write(f"[{seconds_to_hms(line['timestamp'][0])} -> {seconds_to_hms(line['timestamp'][1])}] {line['text']}\n")
            

def download_youtube_audio(
    yt_url: str,
    sub_folders: List[str] = [
        "audio_download",
    ],
) -> str:
    normal_url = r"https://www.youtube.com/watch?v=8tuzFSXeKI0"
    if len(yt_url) > len(normal_url) + 3:
        print(f"網址過長")
        return f"請傳入正常網址"

    try:
        print(f"Start downloading YouTube audio, yt_url={yt_url}")
        base_folder = "./"
        output_folder = os.path.join(base_folder, *sub_folders)
        os.makedirs(output_folder, exist_ok=True)

        file_name_prefix = "tmp_download"
        outtmpl = os.path.join(output_folder, file_name_prefix + ".%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "extract_audio": True,
            "outtmpl": outtmpl,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(yt_url, download=True)
            video_title = info_dict.get("title", "Unknown Title")
            print(f"ori_video_title={video_title}")
            video_title = sanitize_filename(video_title)
            print(f"new_video_title={video_title}")

        tmp_file_name = [
            f for f in os.listdir(output_folder) if f.startswith(file_name_prefix)
        ][0]
        file_format = tmp_file_name.split(".")[-1]

        temp_audio_path = os.path.join(output_folder, tmp_file_name)
        print(f"Selected audio stream: {tmp_file_name}")
        print(f"Downloading audio to {temp_audio_path}")

        timestamp = fetch_cur_timestamp()
        filename_prefix = f"processed_{timestamp}"
        wav_audio_path = os.path.join(
            output_folder, f"{filename_prefix}_{video_title}.wav"
        )
        print(f"Converting {temp_audio_path} to {wav_audio_path}")
        audio = AudioSegment.from_file(temp_audio_path, format=file_format)
        audio.export(wav_audio_path, format="wav")

        # Optionally remove the temporary audio file
        os.remove(temp_audio_path)

        print(f"Download and conversion completed: {wav_audio_path}")
        return wav_audio_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"處理過程中出現錯誤: {str(e)}"
    
def sanitize_filename(name):
    # 去除非字母數字和少數特殊字符外的所有字符
    return "".join(x if x.isalnum() or x in ["_", "-"] else "_" for x in name).strip()

def fetch_cur_timestamp() -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return timestamp


url = 'https://www.youtube.com/watch?v=XDUedunBLrc'
wav_audio_path = download_youtube_audio(yt_url=url)
print(f"path={wav_audio_path}")       
audio_to_transcript(wav_audio_path)