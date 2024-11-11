from typing import Dict, List
import openai
import os
import json
from pydub import AudioSegment
from dotenv import load_dotenv
from file_tracker import ProcessedFileTracker
from pathlib import Path
from openai import OpenAI
from openai.types.audio import TranscriptionCreateResponse

# Load environment variables
load_dotenv()

# Define constants
max_segment_size_mb = 25  # Maximum size per segment in MB
output_dir = "audio_segments"
include_fillers = "Umm, let me think like, hmm... Okay, here's what I'm, like, thinking."
previous_context_window = 100

os.makedirs(output_dir, exist_ok=True)

file_tracker = ProcessedFileTracker()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_unprocessed_audio_files() -> List[Path]:
    with open('config.json', 'r') as f:
        result = json.load(f)
        input_directory_path = result['input_directory']
        dir_path = Path(input_directory_path)
        unprocessed_files = [
            file_path for file_path in dir_path.iterdir()
            if file_path.is_file() and not file_tracker.is_processed(file_path)
        ]
        return unprocessed_files

def calculate_segment_duration(input_audio_file: Path, max_segment_size_mb: int) -> int:
    """Calculate segment duration based on file size to fit within max_segment_size_mb."""
    audio = AudioSegment.from_file(input_audio_file)
    file_size_bytes = os.path.getsize(input_audio_file)
    
    num_segments = max(1, file_size_bytes // (max_segment_size_mb * 1024 * 1024) + 1)
    segment_length_ms = len(audio) // num_segments
    return segment_length_ms

def split_audio_file(input_audio_file: Path, segment_length_ms: int) -> List[str]:
    """Splits audio file into smaller segments and saves them in a subdirectory."""
    audio = AudioSegment.from_file(input_audio_file)
    file_name = Path(input_audio_file).stem
    file_output_dir = os.path.join(output_dir, file_name)
    os.makedirs(file_output_dir, exist_ok=True)
    
    segments = []
    for i in range(0, len(audio), segment_length_ms):
        segment = audio[i:i + segment_length_ms]
        segment_file = os.path.join(file_output_dir, f"{file_name}_segment_{i // segment_length_ms + 1}.mp3")
        segment.export(segment_file, format="mp3")
        segments.append(segment_file)
    
    return segments

import json

def transcribe_with_prompt(segment_path: str, previous_text: str) -> Dict:
    try:
        with open(segment_path, "rb") as audio_file:
            prompt_text = f"{include_fillers} {previous_text}"
            response: TranscriptionCreateResponse = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt=prompt_text,
                response_format="verbose_json"
            )
        # Ensure JSON is parsed correctly
        return json.loads(response.json())  # Explicitly parse JSON string to a dictionary
    except Exception as e:
        print(f"An error occurred during transcription of {segment_path}: {e}")
        return {}


def transcribe_audio_segments_json(segments: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """Transcribe each audio segment and prepare a JSON structure with text, start, and end timestamps."""
    transcription_data = {"segments": []}  # Initialize JSON structure
    previous_text = ""
    
    for segment in segments:
        print(f"Processing segment {segment}")
        transcription: Dict = transcribe_with_prompt(segment, previous_text)
        print(f'Transcription: {transcription}')
        
        if transcription and 'segments' in transcription:
            # Extract start, end, and text from each segment and add to JSON structure
            for seg in transcription["segments"]:
                transcription_data["segments"].append({
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"]
                })
            
            # Update previous_text for context in the next segment
            segment_texts = [seg["text"] for seg in transcription["segments"]]
            previous_text = " ".join(segment_texts)[-previous_context_window:]  # Last 100 chars
        else:
            print(f"Skipping empty transcription for {segment}")
    
    return transcription_data


def process_audio_file(input_audio_file: Path):
    segment_length_ms = calculate_segment_duration(input_audio_file, max_segment_size_mb)
    segments = split_audio_file(input_audio_file, segment_length_ms)
    full_transcription = transcribe_audio_segments_json(segments)
    
    # Save JSON transcription to a file
    file_name = Path(input_audio_file).stem
    transcription_file = os.path.join(output_dir, f"{file_name}_transcription_with_timestamps.json")
    with open(transcription_file, "w") as f:
        json.dump(full_transcription, f, indent=2)  # Directly dump JSON data to file

    file_tracker.mark_processed(input_audio_file)


def main():
    unprocessed_files = get_unprocessed_audio_files()
    for input_audio_file in unprocessed_files:
        print(f"Beginning processing on {input_audio_file}")
        process_audio_file(input_audio_file)

if __name__ == "__main__":
    main()
