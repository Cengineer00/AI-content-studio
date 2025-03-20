from content_creation_tools.core import BaseTask
from content_creation_tools.models.text_to_image import (
    DummyTextToImageModel
)

class TextToImageTask(BaseTask):
    def __init__(self):
        super().__init__("Text-to-Image")

        self.models = [
            DummyTextToImageModel(),
        ]

    def list_models(self):
        return self.models

    def execute(self, model, params, input_data):
        return model.generate(params=params, prompt=input_data)