from content_creation_tools.core import BaseTask
from content_creation_tools.models.text_to_video import (
    DummyTextToVideoModel
)

class TextToVideoTask(BaseTask):
    def __init__(self):
        super().__init__("Text-to-Video")

        self.models = [
            DummyTextToVideoModel(),
        ]

    def list_models(self):
        return self.models

    def execute(self, model, params, input_data):
        return model.generate(params=params, prompt=input_data)
    
    def apply_result(self, result, timestamp):
        filename = f"output/{self.name}_{timestamp}.mp4"
        print(f"\n✓ Would be saved to:\n{filename}")