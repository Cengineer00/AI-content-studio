from content_creation_tools.core import BaseModel

import argparse
import time
import pyautogui
from pynput import keyboard
from typing import Dict, Any


class StableScroll(BaseModel):
    def __init__(self):
        super().__init__("StableScroll Tool")

        self.stop_scrolling = False  # Stop flag
        self.pause_scrolling = False  # Pause state
        
        self.parameter_schema = {
            'scroll_speed': {
                'type': float,
                'description': 'Scroll speed',
                'default': 1.0
            }
        }

    def _on_press(self, key):
        try:
            if key == keyboard.Key.esc:  # Stop scrolling
                self.stop_scrolling = True
                print("Stopped scrolling. Exiting.")

            elif key == keyboard.KeyCode.from_char('s'):  # Pause/resume
                self.pause_scrolling = not self.pause_scrolling
                print("Paused" if self.pause_scrolling else "Resumed")

            elif key == keyboard.Key.up:  # Increase speed
                self.scroll_speed = self.scroll_speed + 0.5  # Keep sign, increase magnitude
                print(f"Increased speed: {self.scroll_speed}")

            elif key == keyboard.Key.down:  # Decrease speed
                self.scroll_speed = self.scroll_speed - 0.5  # Keep sign, decrease magnitude
                print(f"Decreased speed: {self.scroll_speed}")

        except AttributeError:
            pass  # Handles non-character keys

    def generate(self, params: Dict[str, Any]):
        """
        Smooth scrolling using pyautogui.scroll().
        Automatically reverses when speed changes sign.

        Parameters:
        params[scroll_speed] (float): Scroll speed.
        """

        self.scroll_speed = params.get("scroll_speed", 1.0)

        base_interval = 0.1  # Base sleep time for smooth scrolling
        last_sign = 1 if self.scroll_speed > 0 else -1  # Track sign changes

        print("Smooth scrolling started. Controls:")
        print("- ESC to stop")
        print("- Press 'S' to pause/resume")
        print("- Up Arrow to increase speed (scroll up)")
        print("- Down Arrow to decrease speed (scroll down)")
        print(f"Initial speed: {self.scroll_speed}")

        listener = keyboard.Listener(on_press=self._on_press)
        listener.start()

        while not self.stop_scrolling:
            if not self.pause_scrolling:
                current_sign = 1 if self.scroll_speed > 0 else -1  # Check current sign

                # Reverse scroll direction automatically if the sign changes
                if current_sign != last_sign:
                    print(f"Reversing direction: {'Up' if current_sign > 0 else 'Down'}")
                    last_sign = current_sign  # Update last sign

                if self.scroll_speed == 0: continue  # Skip if speed is zero
                interval = base_interval / abs(self.scroll_speed)  # Adjust smoothness
                pyautogui.scroll(current_sign)  # Scroll in the correct direction
                time.sleep(interval)

        listener.stop()

    def get_input(self):
        pass

if __name__ == '__main__':
    stable_scroller = StableScroll()
    params = {
        "scroll_speed": 2.0,
    }
    stable_scroller.generate(params)