from pathlib import Path
from audio_processor import AudioProcessor
from transcription_processor import TranscriptionProcessor
from file_tracker import ProcessedFileTracker
import json


class PipelineManager:
    def __init__(self, audio_processor: AudioProcessor, transcription_processor: TranscriptionProcessor, file_handler: ProcessedFileTracker):
        self.audio_processor = audio_processor
        self.transcription_processor = transcription_processor
        self.file_handler = file_handler

    def process_audio_file(self, input_audio_file: Path, output_dir):
        file_name = input_audio_file.stem
        transcription_file = Path(output_dir) / f"{file_name}.json"

        segment_length_ms = self.audio_processor.calculate_segment_duration(input_audio_file)
        print(f"Calculating segments for {input_audio_file}...")
        segments = self.audio_processor.split_audio_file(input_audio_file, segment_length_ms)
        print(f"Calculated a total of {len(segments)} for {input_audio_file}")

        print(f"Transcribing segments for {input_audio_file}...")
        full_transcription = self.transcription_processor.transcribe_audio_segments(segments)

        file_name = input_audio_file.stem
        transcription_file = Path(output_dir) / f"{file_name}.json"
        print(f"Writing transcription for {input_audio_file} to file {transcription_file}")
        with open(transcription_file, "w") as f:
            json.dump(full_transcription, f, indent=2)

        self.file_handler.mark_processed(input_audio_file)


    def begin_processing(self, audio_files, output_directory):
        for file in audio_files:
            print(f"Starting processing on {file} and will output to {output_directory}")
            self.process_audio_file(file, output_directory)

    def run(self):
        # Get the seperate directories we need
        current_file_directory = Path(__file__).parent.resolve()
        self.config_file_path = current_file_directory.parent / 'config.json'
        with open(self.config_file_path, 'r') as f:
            config = json.load(f)
            programming_directory = config['programming_directory']
            programming_output_directory = config['programming_output_directory']
            interview_directory = config['interview_directory']
            interview_output_directory = config['interview_output_directory']

        unprocessed_programming_files = self.file_handler.get_unprocessed_audio_files(programming_directory)
        unprocessed_interview_files = self.file_handler.get_unprocessed_audio_files(interview_directory)

        self.begin_processing(unprocessed_programming_files, programming_output_directory)
        self.begin_processing(unprocessed_interview_files, interview_output_directory)
