from content_creation_tools.core import BaseModel
from typing import Dict, Any
import os

class DummyImageToVideoModel(BaseModel):
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
        while True:
            input_path = input("Enter input file path: ")
            if os.path.exists(input_path):
                return input_path
            else:
                print("File path does not exist. Please try again.")

    def generate(self, params: Dict[str, Any], image_path: str) -> str:
        print(f"Generating dummy video from the image: {image_path} and params: {params}")
        
        return "dummy video"