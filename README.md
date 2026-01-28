# Hand Gesture Control for Hill Climb Racing

A real-time computer vision system that uses **MediaPipe** to control *Hill Climb Racing* (or similar games) using hand gestures.

## Features
- **Gas (Right Arrow)**: Extend **Index Finger** only.
- **Brake (Left Arrow)**: Make a **Fist**.
- **Idle (Release Keys)**: Open Palm.
- **Stability Control**: Prevents key flickering with a 150ms delay.
- **Visual Feedback**: Real-time webcam feed with landmark drawing and gesture status.

## Prerequisites
- Python 3.x
- Webcam

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Amish-03/mediapipe_hill_climb.git
   cd mediapipe_hill_climb
   ```

2. Install dependencies:
   ```bash
   pip install opencv-python mediapipe numpy pynput
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. The webcam window will open.
3. Bring the game window to the foreground.
4. Use gestures to control the vehicle!

## Troubleshooting
- Ensure good lighting for better detection.
- Run as Administrator if the game ignores key presses.
