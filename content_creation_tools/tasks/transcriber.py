from content_creation_tools.core import BaseTask
from content_creation_tools.models.transcriber import (
    FasterWhisper
)

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