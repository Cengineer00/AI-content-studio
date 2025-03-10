from content_creation_tools.models.text_to_video import (
    DummyTextToVideoModel
)

class TextToVideoTask:
    def __init__(self):
        self.models = {
            'DummyTextToVideoModel': DummyTextToVideoModel(),
        }

    def list_models(self):
        return list(self.models.keys())

    def get_model(self, model_name):
        return self.models.get(model_name)

    def execute(self, model, params, prompt):
        return model.generate(prompt, params)