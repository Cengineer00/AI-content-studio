from content_creation_tools.core import BaseTask
from content_creation_tools.models.type_flow import (
    TypeFlow
)

class TypeFlowTask(BaseTask):
    def __init__(self):
        super().__init__("TypeFlow")

        self.model = TypeFlow()

    def get_model(self):
        return self.model

    def execute(self, model: TypeFlow, params, input_data):
        return model.generate(params=params, text=input_data)
    
    def handle_result(self, result, timestamp):
        pass