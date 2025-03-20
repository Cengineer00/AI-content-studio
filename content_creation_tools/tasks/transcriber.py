from content_creation_tools.models.transcriber import (
    FasterWhisper
)

class TranscriberTask:
    def __init__(self):
        self.models = {
            'FasterWhisper': FasterWhisper(),
        }

    def list_models(self):
        return list(self.models.keys())

    def get_model(self, model_name):
        return self.models.get(model_name)

    def execute(self, model, params, input_data):
        return model.generate(params=params, audio=input_data)