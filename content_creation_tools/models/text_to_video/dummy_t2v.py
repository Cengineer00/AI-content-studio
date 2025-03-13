from content_creation_tools.core import BaseModel
from typing import Dict, Any

class DummyTextToVideoModel(BaseModel):
    def __init__(self):
        super().__init__("Dummy Text-to-Image Model")
        
        self.parameter_schema = {
            'steps': {
                'type': int,
                'description': 'Number of generation steps',
                'default': 50
            },
            'guidance_scale': {
                'type': float,
                'description': 'Guidance scale for text alignment',
                'default': 7.5
            },
            'width': {
                'type': int,
                'description': 'Image width',
                'default': 512
            },
            'height': {
                'type': int,
                'description': 'Image height',
                'default': 512
            }
        }
        
        self.required_params = ['steps']

    def get_input(self) -> str:
        prompt_input = input("Enter a creative prompt: ")
        return prompt_input

    def generate(self, params: Dict[str, Any], prompt: str) -> str:
        print(f"Generating dummy video with prompt: {prompt} and params: {params}")
        
        return "dummy video"