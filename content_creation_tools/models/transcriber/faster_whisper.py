from content_creation_tools.core import BaseModel
from content_creation_tools.utils import write_srt_file

from faster_whisper import WhisperModel
from typing import Dict, Any, BinaryIO, Union, List, Tuple
from numpy import ndarray

class FasterWhisper(BaseModel):
    def __init__(self):
        super().__init__("FasterWhisper Transcriber")

        self.model = None
        
        self.parameter_schema = {
            'model_size_or_path': {
                'type': str,
                'description': 'Size of the model to use, a path to a converted model directory, or a CTranslate2-converted Whisper model ID from the HF Hub.',
                'default': 'medium'
            },
            'device': {
                'type': str,
                'description': 'Device to use for computation ("cpu", "cuda", "auto").',
                'default': 'auto'
            },
            'language': {
                'type': str,
                'description': 'The language spoken in the audio such as "en" or "fr". If not set, the language will be detected in the first 30 seconds of audio.',
                'default': 'tr'
            },
            'log_progress': {
                'type': bool,
                'description': 'Whether to log progress to the console.',
                'default': False
            },
            'max_initial_timestamp': {
                'type': float,
                'description': 'The initial timestamp cannot be later than this.',
                'default': 10
            },
            'max_chars_per_line': {
                'type': int,
                'description': 'Maximum number of characters per line in the subtitles.',
                'default': 20
            },
            'output_file': {
                'type': str,
                'description': 'Path to the output file.',
                'default': 'examples/output.srt'
            }
        }

    def get_input(self) -> str:
        audio = input("Path to the input file: ")
        return audio
    
    def generate(self, params: Dict[str, Any], audio: Union[str, BinaryIO, ndarray]) -> List[Tuple[float, float, str]]:
        if self.model is None:
            print("\t╭─ Initializing the model...")
            print(f"\tParameters: {params}")
            self.model = WhisperModel(params['model_size_or_path'], device=params['device'])

        print("\t╭─ Transcribing the audio...")
        transcribe_result, info = self.model.transcribe(
            audio=audio,
            word_timestamps=True,
            language=params['language'],
            log_progress=params['log_progress'],
            max_initial_timestamp=params['max_initial_timestamp']
        )
        transcribe_result = list(transcribe_result)  # The transcription will actually run here.

        # Convert result to a list of tuples
        segments = []
        for segment in transcribe_result:
            for word in segment.words:
                segments.append((word.start, word.end, word.word))
    
        merged_segments = self._merge_segments(segments, max_chars_per_line=params['max_chars_per_line'])

        write_srt_file(merged_segments, params['output_file'])

        return merged_segments

    def _merge_segments(self, segments: List, max_chars_per_line: int = 30) -> List[Tuple[float, float, str]]:
        lines = []
        current_line = ""
        current_start = segments[0][0]
        for i in range(len(segments)):
            current_word = segments[i]
            next_word = segments[i + 1] if i + 1 < len(segments) else None

            # Check if next word will exceed the max_chars_per_line or current_word ends with punctuation
            if next_word is not None and (len(current_line) + len(next_word[2]) > max_chars_per_line or current_word[2].endswith((",", ".", "!", "?"))):
                line = current_line + current_word[2].strip()
                lines.append([current_start, current_word[1], line])
                current_line = ""
                current_start = next_word[0]
                continue
            current_line += current_word[2].strip() + " "
                
        # Add the last line
        if current_line:
            lines.append([current_start, current_word[1], current_line])
        return lines