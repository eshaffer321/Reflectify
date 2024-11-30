from typing import List
from pathlib import Path
from pydub import AudioSegment
import os


class AudioProcessor:
    def __init__(self, max_segment_size_mb: int, output_dir: str):
        self.max_segment_size_mb = max_segment_size_mb
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def calculate_segment_duration(self, input_audio_file: Path) -> int:
        audio = AudioSegment.from_file(input_audio_file)
        file_size_bytes = os.path.getsize(input_audio_file)
        num_segments = max(1, file_size_bytes // (self.max_segment_size_mb * 1024 * 1024) + 1)
        return len(audio) // num_segments

    def split_audio_file(self, input_audio_file: Path, segment_length_ms: int) -> List[str]:
        audio = AudioSegment.from_file(input_audio_file)
        file_name = input_audio_file.stem
        file_output_dir = os.path.join(self.output_dir, file_name)
        os.makedirs(file_output_dir, exist_ok=True)

        segments = []
        for i in range(0, len(audio), segment_length_ms):
            segment = audio[i:i + segment_length_ms]
            segment_file = os.path.join(file_output_dir, f"{file_name}_segment_{i // segment_length_ms + 1}.mp3")
            segment.export(segment_file, format="mp3")
            segments.append(segment_file)

        return segments
    
    