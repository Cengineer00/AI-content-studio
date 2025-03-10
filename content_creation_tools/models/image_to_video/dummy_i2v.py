from content_creation_tools.core import BaseModel
from typing import Dict, Any

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

    def generate(self, prompt: str, params: Dict[str, Any]) -> str:
        validated_params = self.validate_parameters(params)
        
        print(f"Generating dummy video with prompt: {prompt} and params: {validated_params}")
        
        return "dummy video"