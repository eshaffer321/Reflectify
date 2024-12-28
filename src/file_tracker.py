import json
import os
from pathlib import Path
from typing import Dict, Union, List

class ProcessedFileTracker:
    def __init__(self, file_path: str = "processed_files.json"):
        # Get the directory where the current script resides
        current_file_directory = Path(__file__).parent.resolve()

        # Construct the path to the config file relative to the script's directory
        self.config_file_path = current_file_directory.parent / 'config.json'

        self.file_path: str = file_path
        self.data: Dict[str, str] = {}  # Dictionary to track processed files
        self._load_data()

    def _load_data(self) -> None:
        """Loads the processed files data from JSON."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {self.file_path} is not a valid JSON file. Initializing with an empty dictionary.")
                self.data = {}  # Initialize as empty if JSON is invalid
        else:
            self.data = {}

    def _save_data(self) -> None:
        """Saves the processed files data to JSON."""
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def is_processed(self, filename: Union[str, Path]) -> bool:
        """Checks if a file has been processed.

        Args:
            filename: The name or path of the file to check.

        Returns:
            True if the file is marked as processed; False otherwise.
        """
        return str(filename) in self.data

    def mark_processed(self, filename: Union[str, Path]) -> None:
        """Marks a file as processed.

        Args:
            filename: The name or path of the file to mark as processed.
        """
        self.data[str(filename)] = "processed"
        self._save_data()

    def get_unprocessed_audio_files(self, input_directory_path) -> List[Path]:

        dir_path = Path(input_directory_path)
        if not dir_path.exists():
            raise FileNotFoundError(f"Input directory '{input_directory_path}' does not exist.")

        # Return a list of unprocessed files
        unprocessed_files = [
            file_path for file_path in dir_path.iterdir()
            if file_path.is_file() and not self.is_processed(file_path)
        ]
        print(f'Found {len(unprocessed_files)} unprocessed audio file(s) in {input_directory_path}')
        return unprocessed_files