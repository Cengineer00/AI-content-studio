from content_creation_tools.core import BaseModel
import pyautogui
import time
from typing import Dict, Any

class TypeFlow(BaseModel):
    def __init__(self):
        super().__init__("TypeFlow Tool")
        
        self.parameter_schema = {
            'pause_char': {
                'type': float,
                'description': 'Seconds between characters',
                'default': 0.05
            },
            'pause_punc': {
                'type': float,
                'description': 'Seconds pause at punctuation',
                'default': 1.0
            }
        }
        
    def get_input(self) -> str:
        """
        Asks the user for input. They can either:
        1. Type the text directly, or
        2. Provide the path to a text file.
        """
        print(f"Welcome to the {self.name}!")
        choice = input("Do you want to (1) type the text or (2) provide a file path? Enter 1 or 2: ").strip()

        if choice == "1":
            # User types the text directly
            print("Enter your text (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            text = "\n".join(lines)
        elif choice == "2":
            # User provides a file path
            file_path = input("Enter the path to the text file: ").strip()
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
            except FileNotFoundError:
                print("Error: File not found. Please check the path and try again.")
                return None
        else:
            print("Invalid choice. Please enter 1 or 2.")
            return None

        return text
    
    def generate(self, params: Dict[str, Any], text: str):
        """
        Simulates typing text with a natural typing effect.

        Parameters:
        params[pause_char] (float): Seconds between characters (default: 0.05).
        params[pause_punc] (float): Seconds pause at punctuation (default: 1.0).
        text (str): The pre-written text to type.
        """

        pause_char = params.get("pause_char", 0.05)
        pause_punc = params.get("pause_punc", 1.0)

        # Wait for 3 seconds to allow the user to focus on the target input field
        print("Starting in 3 seconds... Focus on the input field!")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("Go!")

        for char in text:
            if char == "\n":  # If it's a new line, press Enter
                pyautogui.press("enter")
                time.sleep(pause_char)  # Small delay after pressing Enter
            else:
                pyautogui.write(char)  # Simulate typing the character
                if char in '.!?':
                    time.sleep(pause_punc)  # Pause at punctuation
                else:
                    time.sleep(pause_char)  # Normal typing speed

# Main program
if __name__ == "__main__":
    type_flow = TypeFlow()
    text = type_flow.get_input()
    if text:
        params = {
            "pause_char": 0.03,
            "pause_punc": 0.1
        }
        type_flow.generate(params, text)