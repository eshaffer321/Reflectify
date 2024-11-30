from pathlib import Path
from audio_processor import AudioProcessor
from transcription_processor import TranscriptionProcessor
from file_tracker import ProcessedFileTracker
import json


class PipelineManager:
    def __init__(self, audio_processor: AudioProcessor, transcription_processor: TranscriptionProcessor, file_handler: ProcessedFileTracker, output_dir: str):
        self.audio_processor = audio_processor
        self.transcription_processor = transcription_processor
        self.file_handler = file_handler
        self.output_dir = output_dir

    def process_audio_file(self, input_audio_file: Path):
        segment_length_ms = self.audio_processor.calculate_segment_duration(input_audio_file)
        print("Calculating segments...")
        segments = self.audio_processor.split_audio_file(input_audio_file, segment_length_ms)
        print("Transcribing segments...")
        full_transcription = self.transcription_processor.transcribe_audio_segments(segments)

        file_name = input_audio_file.stem
        print("Writing transcription to file...")
        transcription_file = Path(self.output_dir) / f"{file_name}_transcription_with_timestamps.json"
        with open(transcription_file, "w") as f:
            json.dump(full_transcription, f, indent=2)

        self.file_handler.mark_processed(input_audio_file)

    def run(self):
        unprocessed_files = self.file_handler.get_unprocessed_audio_files()
        for input_audio_file in unprocessed_files:
            print(f"************** STARTING {input_audio_file} ********************")
            self.process_audio_file(input_audio_file)
            print(f"************** FINISHED {input_audio_file} ********************")