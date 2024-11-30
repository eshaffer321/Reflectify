# Reflectify

Reflectify is a tool designed to help you reflect on and iterate upon your interview practice. It automates the process of transcribing recorded interview sessions and sets the groundwork for tracking your performance over time. This project is a work in progress with plans for more advanced features, such as in-app feedback and meta-analysis.

## Features

- **Audio Transcription**: Processes audio files from a directory, segments them, and uploads them to the Whisper API for transcription.
- **File Management**: Tracks which audio files have been processed to avoid reprocessing the same files multiple times.
- **Transcription Output**: Combines all audio segments into a single transcription file and saves it locally for easy access.

## Future Roadmap

1. **In-App Feedback**: Integrate ChatGPT for real-time feedback on clarity, correctness, and problem-solving approach.
2. **Prompt Engineering**: Customize prompts for more targeted feedback.
3. **Performance Tracking**: Add meta-analysis tools to monitor progress over time.

## Installation

### Requirements
- Python 3.7+
- [PyDub](https://github.com/jiaaro/pydub) for audio segmentation
- Whisper API access
- Additional Python dependencies (see `requirements.txt`)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/reflectify.git
   cd reflectify
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Whisper API credentials in the `config.py` file.

## Usage

1. Record your audio files and place them in a directory.
2. Run Reflectify:
   ```
   python reflectify.py --input-directory /path/to/audio/files
   ```
3. The program will:
   - Identify audio files in the directory.
   - Split them into smaller segments.
   - Upload the segments to Whisper for transcription.
   - Combine the transcriptions and save the result to a file.
   - Mark processed files to avoid reprocessing.

4. Review the generated transcription file.

## Example Workflow

1. Record a mock interview session.
2. Run Reflectify to generate a transcription.
3. Use the transcription for self-review or manually upload it to ChatGPT for feedback.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality or add new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PyDub**: For making audio segmentation straightforward.
- **ChatGPT Whisper API**: For transcription services.
- **Inspiration**: To continually improve and master the art of interviewing.
