from content_creation_tools.utils.stable_scroll import (
    StableScroll
)

class StableScrollTask:
    def __init__(self):
        self.model = StableScroll()

    def get_model(self):
        return self.model

    def execute(self, model: StableScroll, params, input_data):
        return model.generate(params=params)