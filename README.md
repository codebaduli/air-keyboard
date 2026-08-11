# Air Keyboard

A computer-vision-based virtual keyboard that allows users to interact with a keyboard interface using hand gestures, without physically touching a keyboard.

## Project Overview

Air Keyboard is a gesture-controlled keyboard project built using Python and computer vision.

The project uses a camera to capture the user's hand movements and processes the hand landmarks to detect gestures and determine user input.

The main idea is to create a touchless keyboard interaction system where hand movements can be translated into keyboard actions.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Computer Vision
- Hand Landmark Detection

## How It Works

The system follows a pipeline for processing the user's hand movement:

1. Capture video from the camera.
2. Detect the hand using MediaPipe.
3. Extract hand landmarks.
4. Process the landmark coordinates.
5. Calculate the required distances between landmarks.
6. Apply gesture detection logic.
7. Use hysteresis to make gesture detection more stable.
8. Convert the detected gesture into keyboard input.

## Project Evolution

### Initial Approach — Angle-Based Detection

The initial version of the project used angles between hand landmarks to determine gestures.

Although this approach worked in some situations, it had limitations.

Small changes in finger orientation could cause significant changes in the calculated angle. This made the detection sensitive to hand rotation and natural variations in finger movement.

### Transition to Distance-Based Detection

To make the detection more stable, the approach was changed from angle-based detection to distance-based detection.

Instead of relying primarily on the angle between landmarks, the system compares distances between relevant hand landmarks.

This provides a simpler and more robust way of determining whether fingers are sufficiently close to or far from particular positions.

### Hysteresis

Hysteresis was introduced to reduce unstable switching between gesture states.

Without hysteresis, small fluctuations in landmark positions can repeatedly switch a gesture between states.

For example:

```text
Detected → Not Detected → Detected → Not Detected
```

even when the user's finger is almost stationary.

Using different thresholds for entering and leaving a state makes the detection more stable.

Processing Pipeline
```text
The project follows a sequence of processing stages:

            Camera
            ↓
            Frame Capture
            ↓
            Hand Detection
            ↓
            Landmark Extraction
            ↓
            Distance Calculation
            ↓
            Gesture Detection
            ↓
            Hysteresis / Stabilization
            ↓
            Keyboard Action

Each stage processes the output of the previous stage before passing it to the next stage.


Current Project Structure
air-keyboard/
│
├── camera.py
├── hand.py
├── test.py
├── .gitignore
└── README.md
Installation
```

Clone the repository:`git clone https://github.com/codebaduli/air-keyboard.git`

Move into the project directory:`cd air-keyboard`

Create a virtual environment:`python -m venv venv`

Activate it on Windows:`venv\Scripts\activate`

Install the required dependencies:
`pip install opencv-python mediapipe`
Running the Project

After activating the virtual environment, run the required Python file:``python camera.py`

The exact file used to start the application may change as the project develops.

Future Improvements:
  1. Improve gesture recognition accuracy.
  2. Add more keyboard actions.
  3. Reduce false gesture detections.
  4. Improve performance and responsiveness.
  5. Add more hand gestures.
  6. Implement a complete virtual keyboard interface.
  7. Improve usability under different lighting conditions.

Learning Outcomes:

Through this project, I explored:

  1. Computer vision
  2. Hand landmark detection
  3. MediaPipe
  4. OpenCV
  5. Coordinate-based gesture recognition
  6. Distance calculations
  7. Threshold-based detection
  8. Hysteresis
  9. Processing pipelines
  10. Debugging and iterative development
  11. Git and GitHub


Author: Gariee


 