from typing import Dict, Any
from abc import ABC, abstractmethod

class BaseTask(ABC):
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    @abstractmethod
    def execute(self, params: Dict[str, Any]):
        """Abstract method to be implemented by subclasses"""
        pass

    @abstractmethod
    def handle_result(self, result, timestamp):
        """Abstract method to be implemented by subclasses"""
        pass