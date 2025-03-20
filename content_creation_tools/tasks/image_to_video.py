from content_creation_tools.core import BaseTask
from content_creation_tools.models.image_to_video import (
    DummyImageToVideoModel
)

class ImageToVideoTask(BaseTask):
    def __init__(self):
        super().__init__("Image-to-Video")

        self.models = [
            DummyImageToVideoModel(),
        ]

    def list_models(self):
        return self.models

    def execute(self, model, params, input_data):
        return model.generate(params=params, image_path=input_data)
    
    def apply_result(self, result, timestamp):
        filename = f"output/{self.name}_{timestamp}.mp4"
        print(f"\n✓ Would be saved to:\n{filename}")