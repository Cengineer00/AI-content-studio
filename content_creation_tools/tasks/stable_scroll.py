from content_creation_tools.core import BaseTask
from content_creation_tools.models.stable_scroll import (
    StableScroll
)

class StableScrollTask(BaseTask):
    def __init__(self):
        super().__init__("StableScroller")

        self.model = StableScroll()

    def get_model(self):
        return self.model

    def execute(self, model: StableScroll, params, input_data):
        return model.generate(params=params)
    
    def handle_result(self, result, timestamp):
        pass