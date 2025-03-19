from content_creation_tools.models.text_to_image import (
    DummyTextToImageModel
)
from typing import Dict, Any

class TextToImageTask:
    def __init__(self):
        self.models = {
            'DummyTextToImageModel': DummyTextToImageModel(),
        }

    def list_models(self):
        return list(self.models.keys())

    def get_model(self, model_name):
        return self.models.get(model_name)

    def execute(self, model, params, input_data):
        return model.generate(params=params, prompt=input_data)