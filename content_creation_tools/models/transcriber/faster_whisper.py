from faster_whisper import WhisperModel
from content_creation_tools.core import BaseModel
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
            }
        }

    def get_input(self) -> str:
        audio = input("Path to the input file: ")
        return audio
    
    def generate(self, params: Dict[str, Any], audio: Union[str, BinaryIO, ndarray]) -> List[Tuple[float, float, str]]:
        if self.model is None:
            print("\t╭─ Initializing the model...")
            self.model = WhisperModel(params['model_size_or_path'], device=params['device'])

        segments, info = self.model.transcribe(
            audio=audio,
            word_timestamps=True,
            language=params['language'],
            log_progress=params['log_progress'],
            max_initial_timestamp=params['max_initial_timestamp']
        )
        segments = list(segments)  # The transcription will actually run here.

        subtitles = []
        for segment in segments:
            for word in segment.words:
                subtitles.append((word.start, word.end, word.word))

        return subtitles