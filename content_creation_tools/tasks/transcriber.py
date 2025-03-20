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
    
    def apply_result(self, result, timestamp):
        """
        Processes subtitle results by either saving as an SRT file, applying to video, or quitting.
        
        Args:
            result (list): List of subtitle tuples in format [(start, end, text), ...]
            timestamp (str): Unique identifier for output filenames
        """
        # Print generated subtitles in readable format
        print("\nGenerated subtitles preview:")
        for idx, (start, end, text) in enumerate(result, 1):
            print(f"{idx:03d}")
            print(f"{start} --> {end}")
            print(f"{text}\n")

        # Get user choice with validation
        while True:
            choice = input("Would you like to:\n"
                        "1. Save as .srt file (enter 'srt')\n"
                        "2. Apply to video using SubtitleStyler (enter 'video')\n"
                        "3. Quit without saving (enter 'q')\n"
                        "Choice: ").lower()
            
            if choice in ('srt', 'video', 'q'):
                break
            print("Invalid input. Please enter 'srt', 'video', or 'q'.")

        if choice == 'srt' or choice == '1':
            # Generate filename and save
            filename = f"output/{self.name}_{timestamp}.srt"
            write_srt_file(result, filename)
            print(f"\n✓ Subtitles successfully saved to:\n{filename}")
        
        elif choice == 'video' or choice == '2':
            # Placeholder for video application logic
            print("\nVideo subtitle application feature is under development.")
        
        elif choice == 'q' or choice == '3':
            print("\nExiting without saving. Goodbye!")