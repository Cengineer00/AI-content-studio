from content_creation_tools.core import BaseTask
from content_creation_tools.models.transcriber import (
    FasterWhisper
)
from content_creation_tools.utils import write_srt_file

class TranscriberTask(BaseTask):
    def __init__(self):
        super().__init__("Transcriber")

        self.models = [
            FasterWhisper(),
        ]

    def list_models(self):
        return self.models

    def execute(self, model, params, input_data):
        return model.generate(params=params, audio=input_data)
    
    def handle_result(self, result: list, timestamp: str):
        """
        Processes subtitle results by saving to output/{self.name}_{timestamp}.srt
        
        Args:
            result (list): List of subtitle tuples in format [(start, end, text), ...]
            timestamp (str): Unique identifier for output filenames
        """
        # Print generated subtitles in readable format
        print("\nGenerated subtitles preview:")
        for idx, (start, end, text) in enumerate(result[:5], 1):
            print(f"{idx:03d}")
            print(f"{start} --> {end}")
            print(f"{text}\n")
        print("...\n")

        # Generate filename and save
        filename = f"output/{self.name}_{timestamp}.srt"
        write_srt_file(result, filename)
        print(f"\n✓ Subtitles successfully saved to:\n{filename}")