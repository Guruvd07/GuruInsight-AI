import os
import re
import subprocess
import requests
import xml.etree.ElementTree as ET
import whisper
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


# -------------------------------------------------
# 1. Extract YouTube Video ID from URL
# -------------------------------------------------
def extract_video_id(url: str) -> str:
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"shorts/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL – Could not extract video ID.")


# -------------------------------------------------
# 2. FASTEST METHOD — YouTube TimedText Transcript
# -------------------------------------------------
def get_timedtext_transcript(video_id: str):
    """
    Fetch transcript using YouTube's public timedtext API.
    Works even when Transcript API is blocked.
    """
    url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang=en"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return None

        if len(response.text.strip()) == 0:
            return None

        transcript_list = []
        root = ET.fromstring(response.text)

        for child in root.findall("text"):
            text = child.text if child.text else ""
            start = float(child.attrib.get("start", 0))
            dur = float(child.attrib.get("dur", 0))

            transcript_list.append({
                "text": text,
                "start": start,
                "duration": dur
            })

        return transcript_list if len(transcript_list) > 0 else None

    except Exception as e:
        print("TimedText fetch error:", e)
        return None


# -------------------------------------------------
# 3. YouTube Transcript API (Fallback #1)
# -------------------------------------------------
def get_yt_transcript(video_id: str):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception:
        return None


# -------------------------------------------------
# 4. Download audio using yt-dlp (Fallback #2)
# -------------------------------------------------
def download_audio(url: str, output_path="audio.mp3"):
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", output_path,
        url
    ]

    try:
        subprocess.run(command, check=True)
        return output_path
    except Exception as e:
        print("Audio download failed:", e)
        return None


# -------------------------------------------------
# 5. Whisper Transcription (Fallback #3)
# -------------------------------------------------
def whisper_transcribe(audio_path: str):
    print("Running Whisper... (this may take time)")

    model = whisper.load_model("tiny")   # MUCH faster than base/large models

    result = model.transcribe(audio_path)

    transcript_list = []
    for seg in result["segments"]:
        transcript_list.append({
            "text": seg["text"],
            "start": seg["start"],
            "duration": seg["end"] - seg["start"]
        })

    return transcript_list


# -------------------------------------------------
# 6. MAIN PIPELINE — FASTEST → Whisper fallback
# -------------------------------------------------
def get_transcript(url: str):
    print("\n--- Extracting Transcript ---")

    video_id = extract_video_id(url)
    print("Video ID:", video_id)

    # 1. Try FAST TimedText
    print("Trying TimedText...")
    timedtext = get_timedtext_transcript(video_id)

    if timedtext:
        print("Transcript found using TimedText!")
        return timedtext

    # 2. Try YouTube Transcript API
    print("Trying YouTube Transcript API...")
    transcript = get_yt_transcript(video_id)

    if transcript:
        print("Transcript found using YouTube API!")
        return transcript

    # 3. Whisper Last Fallback
    print("No transcript found. Using Whisper fallback...")
    audio_path = download_audio(url, "audio.mp3")

    if not audio_path:
        print("Audio download failed. Cannot generate transcript.")
        return None

    whisper_transcript = whisper_transcribe(audio_path)
    return whisper_transcript
