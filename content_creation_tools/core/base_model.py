from typing import Dict, Any
from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, name: str):
        self.name = name
        self.parameter_schema: Dict[str, Dict[str, Any]] = {}
        self.required_params: list = []

    def get_parameter_help(self) -> str:
        """Generate help text for model parameters"""
        help_text = f"\n{self.name} Parameters:\n"
        help_text += "{:<20} {:<15} {:<30} {:<10}\n".format(
            "Parameter", "Type", "Description", "Default"
        )
        
        for param, info in self.parameter_schema.items():
            help_text += "{:<20} {:<15} {:<30} {:<10}\n".format(
                param,
                info.get('type', 'any').__name__,
                info.get('description', 'No description'),
                str(info.get('default', 'None'))
            )
        return help_text

    def validate_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and convert parameters according to schema"""
        validated = {}
        errors = []

        # Check required parameters
        for param in self.required_params:
            if param not in params and 'default' not in self.parameter_schema.get(param, {}):
                errors.append(f"Missing required parameter: {param}")

        # Validate parameters
        for param, value in params.items():
            if param not in self.parameter_schema:
                errors.append(f"Invalid parameter: {param}")
                continue

            schema = self.parameter_schema[param]
            try:
                # Convert type if specified
                if 'type' in schema:
                    validated[param] = schema['type'](value)
                else:
                    validated[param] = value
            except (ValueError, TypeError):
                errors.append(f"Invalid type for {param}. Expected {schema.get('type', 'any')}")

        # Apply defaults for missing optional parameters
        for param, schema in self.parameter_schema.items():
            if param not in validated and 'default' in schema:
                validated[param] = schema['default']

        if errors:
            raise ValueError("\n".join(errors))
            
        return validated

    @abstractmethod
    def generate(self, prompt: str, params: Dict[str, Any]) -> str:
        """Abstract method to be implemented by subclasses"""
        pass