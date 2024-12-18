from typing import Dict, List
import os
import json
from pydub import AudioSegment
from dotenv import load_dotenv
from file_tracker import ProcessedFileTracker
from pathlib import Path
from pipeline_manager import PipelineManager
from audio_processor import AudioProcessor
from transcription_processor import TranscriptionProcessor 
from openai import OpenAI
from openai.types.audio import TranscriptionCreateResponse

# Load environment variables
load_dotenv()

# Define constants
max_segment_size_mb = 25  # Maximum size per segment in MB
output_dir = "data/audio_segments"
previous_context_window = 100

os.makedirs(output_dir, exist_ok=True)

file_tracker = ProcessedFileTracker()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def main():

    PipelineManager(
        AudioProcessor(max_segment_size_mb, output_dir),
        TranscriptionProcessor(client, previous_context_window),
        ProcessedFileTracker(),
        output_dir).run()

if __name__ == "__main__":
    main()
