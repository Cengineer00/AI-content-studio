from content_creation_tools.core import BaseTask
from content_creation_tools.models.subtitle_styler import (
    SubtitleStyler
)

from moviepy import CompositeVideoClip


class SubStylerTask(BaseTask):
    def __init__(self):
        super().__init__("SubtitleStyler")

        self.model = SubtitleStyler()

    def get_model(self):
        return self.model

    def execute(self, model: SubtitleStyler, params, input_data):
        return model.generate(params=params, video_path=input_data["video_path"], subtitle_path=input_data["subtitle_path"])
    
    def handle_result(self, result: CompositeVideoClip, timestamp: str):
        """
        Processes subtitle added CompositeVideoClip by saving to output/{self.name}_{timestamp}.mp4
        
        Args:
            result (CompositeVideoClip): Video with subtitles added
            timestamp (str): Unique identifier for output filenames
        """

        print(f"\n✓ Subtitles successfully added to video.")
        output_path = f"output/{self.name}_{timestamp}.mp4"
        result.write_videofile(output_path, fps=result.fps, codec="libx264")
        print(f"\n✓ Video successfully saved to:\n{output_path}")