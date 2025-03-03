import argparse
import time
import pyautogui
from pynput import keyboard

stop_scrolling = False  # Global flag
pause_scrolling = False  # Pause state
scroll_speed = 1.0  # Default speed

def on_press(key):
    global stop_scrolling, pause_scrolling, scroll_speed

    try:
        if key == keyboard.Key.esc:  # Stop scrolling
            stop_scrolling = True
            print("Stopped scrolling. Exiting.")

        elif key == keyboard.KeyCode.from_char('s'):  # Pause/resume
            pause_scrolling = not pause_scrolling
            print("Paused" if pause_scrolling else "Resumed")

        elif key == keyboard.Key.up:  # Increase speed
            scroll_speed = scroll_speed + 0.5  # Keep sign, increase magnitude
            print(f"Increased speed: {scroll_speed}")

        elif key == keyboard.Key.down:  # Decrease speed
            scroll_speed = scroll_speed - 0.5  # Keep sign, decrease magnitude
            print(f"Decreased speed: {scroll_speed}")

    except AttributeError:
        pass  # Handles non-character keys

def smooth_scroll():
    """
    Smooth scrolling using pyautogui.scroll().
    Automatically reverses when speed changes sign.
    """
    global stop_scrolling, pause_scrolling, scroll_speed

    base_interval = 0.1  # Base sleep time for smooth scrolling
    last_sign = 1 if scroll_speed > 0 else -1  # Track sign changes

    print("Smooth scrolling started. Controls:")
    print("- ESC to stop")
    print("- Space to pause/resume")
    print("- Up Arrow to increase speed (scroll up)")
    print("- Down Arrow to decrease speed (scroll down)")
    print(f"Initial speed: {scroll_speed}")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while not stop_scrolling:
        if not pause_scrolling:
            current_sign = 1 if scroll_speed > 0 else -1  # Check current sign

            # Reverse scroll direction automatically if the sign changes
            if current_sign != last_sign:
                print(f"Reversing direction: {'Up' if current_sign > 0 else 'Down'}")
                last_sign = current_sign  # Update last sign

            if scroll_speed == 0: continue  # Skip if speed is zero
            interval = base_interval / abs(scroll_speed)  # Adjust smoothness
            pyautogui.scroll(current_sign)  # Scroll in the correct direction
            time.sleep(interval)

    listener.stop()

def main():
    parser = argparse.ArgumentParser(description="Smooth scroll with keyboard controls.")
    parser.add_argument("--speed", type=float, default=1.0, help="Initial scroll speed (default: 1.0)")
    args = parser.parse_args()

    global scroll_speed
    scroll_speed = args.speed

    smooth_scroll()

if __name__ == '__main__':
    main()
