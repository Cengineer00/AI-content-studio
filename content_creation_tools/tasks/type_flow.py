from content_creation_tools.core import BaseTask
from content_creation_tools.models.type_flow import (
    TypeFlow
)

class TypeFlowTask:
    def __init__(self):
        self.model = TypeFlow()

    def get_model(self):
        return self.model

    def execute(self, model: TypeFlow, params, input_data):
        return model.generate(params=params, text=input_data)