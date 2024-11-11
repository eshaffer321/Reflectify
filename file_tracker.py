import json
import os
from pathlib import Path
from typing import Dict, Union

class ProcessedFileTracker:
    def __init__(self, file_path: str = "processed_files.json"):
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
            json.dump(self.data, f)

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
