import json
from typing import Dict, List
from openai import OpenAI
from openai.types.audio import TranscriptionCreateResponse


class TranscriptionProcessor:
    def __init__(self, client: OpenAI, previous_context_window: int = 100):
        self.client = client
        self.previous_context_window = previous_context_window

    def transcribe_with_prompt(self, segment_path: str, previous_text: str) -> Dict[str,str]:
        try:
            with open(segment_path, "rb") as audio_file:
                prompt_text = f"{previous_text}"
                response: TranscriptionCreateResponse = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    prompt=prompt_text
                )
            return json.loads(response.model_dump_json())
        except Exception as e:
            print(f"An error occurred during transcription of {segment_path}: {e}")
            return {}

    def transcribe_audio_segments(self, segments: List[str]) -> Dict[str,str]:
        transcription_data = {"text": ""}
        previous_text = ""

        for segment in segments:
            print(f"Processing segment {segment}")
            transcription: Dict[str,str] = self.transcribe_with_prompt(segment, previous_text)

            if transcription:
                transcription_data["text"] += transcription["text"]

                previous_text = transcription_data["text"][-self.previous_context_window:]
            else:
                print(f"Skipping empty transcription for {segment}")

        return transcription_data