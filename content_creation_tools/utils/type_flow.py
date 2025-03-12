import pyautogui
import time

def type_flow(text, pause_char=0.05, pause_punc=1.0):
    """
    Simulates typing text with a natural typing effect.

    Parameters:
    text (str): The pre-written text to type.
    pause_char (float): Seconds between characters (default: 0.05).
    pause_punc (float): Seconds pause at punctuation (default: 1.0).
    """
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

def get_user_input():
    """
    Asks the user for input. They can either:
    1. Type the text directly, or
    2. Provide the path to a text file.
    """
    print("Welcome to the TypeFlow Tool!")
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

# Main program
if __name__ == "__main__":
    text = get_user_input()
    if text:
        type_flow(text, pause_char=0.03, pause_punc=0.1)