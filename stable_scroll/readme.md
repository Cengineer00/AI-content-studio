Smooth Scrolling with Keyboard Controls
This Python script enables smooth scrolling using the pyautogui library, with interactive keyboard controls for adjusting the speed and direction. It also supports pausing and resuming the scrolling.

Features
Smooth Scrolling: Uses pyautogui.scroll() to scroll continuously, with adjustable speed.
Pause/Resume: Toggle the scrolling pause/resume with the "S" key.
Speed Adjustment: Increase or decrease scrolling speed using Up and Down arrow keys.
Automatic Direction Reversal: The direction of scrolling reverses automatically when the speed changes its sign.
Stop: Stop scrolling and exit the script with the "ESC" key.


# Smooth Scrolling with Keyboard Controls

This Python script enables smooth scrolling using the pyautogui library, with interactive keyboard controls for adjusting the speed and direction. It also supports pausing and resuming the scrolling.

A Python script to scroll up or down at a constant speed. The script allows continuous scrolling and can be stopped by pressing the **ESC** key.

## Features
- Smooth Scrolling: Scroll smoothly with adjustable speed.
- Pause/Resume: Toggle the scrolling pause/resume with the **S** key.
- Speed Adjustment: Increase or decrease scrolling speed using Up and Down arrow keys.
- Automatic Direction Reversal: The direction of scrolling reverses automatically when the speed changes its sign.
- Stop: Stop scrolling and exit the script with the **ESC** key.
- Scroll continuously at a specified speed (positive for up, negative for down).
- Uses the **ESC** key to stop scrolling.

## Requirements
Ensure you have Python installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage
```bash
python scroll.py --speed -2
```

### Arguments:
- --speed: Set the initial scroll speed (default: 1.0)



## License
This project is open-source. Feel free to modify it and use it for personal purposes.