# Hand Gesture Controlled Robot

Control an Arduino-based robot car with hand gestures detected through a webcam. Python uses OpenCV and MediaPipe to count raised fingers, then sends a command to the Arduino over USB serial.

## Features

- Real-time hand and finger detection
- Forward, backward, left, right, stop, and horn controls
- Arduino serial communication at 9600 baud
- Automatic stop command when the program closes
- Support for either left or right hand

## Hardware

- Arduino Uno or compatible board
- L298N motor driver
- DC geared motors and robot chassis
- Webcam
- Separate battery supply for the motors
- Optional LED or buzzer

> [!IMPORTANT]
> Connect the Arduino **GND** and L298N **GND** together. Do not rely on USB power to run the motors. A fully charged motor battery pack is recommended.

## Gesture Commands

| Raised fingers | Serial command | Robot action |
| ---: | :---: | --- |
| 0 | `0` | Stop |
| 1 | `1` | Move forward |
| 2 | `2` | Move backward |
| 3 | `3` | Turn right |
| 4 | `4` | Turn left |
| 5 | `5` | Honk |

## Wiring

| L298N pin | Arduino pin | Purpose |
| --- | --- | --- |
| ENA | D5 | Left motor speed (PWM) |
| IN1 | D6 | Left motor direction |
| IN2 | D7 | Left motor direction |
| ENB | D10 | Right motor speed (PWM) |
| IN3 | D8 | Right motor direction |
| IN4 | D9 | Right motor direction |
| GND | GND | Common ground |
| LED1 / Buzzer | D2 | Horn output |
| LED2 | D3 | Optional indicator |

If forward/backward or left/right is reversed on your physical robot, reverse that motor's two output wires on the L298N, or adjust the matching motor function in `gesture_robot.ino`.

## Project Structure

```text
.
├── gesture_controller.py      # Runs the detector and sends serial commands
├── hand_gesture_detector.py   # Webcam and MediaPipe hand tracking
├── gesture_robot.ino          # Arduino firmware
├── requirements.txt           # Python dependencies
└── .gitignore
```

## Installation

1. Upload `gesture_robot.ino` using the Arduino IDE.
2. Connect the Arduino to the computer with USB.
3. Check the board's serial port and update `SERIAL_PORT` in `gesture_controller.py` if needed. On Windows, it will look like `COM14`.
4. Install the Python packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Start the project:

   ```bash
   python gesture_controller.py
   ```

Press **Q** in the camera window or **Ctrl+C** in the terminal to exit. The controller sends a final stop command before it closes.

## Troubleshooting

| Problem | Check |
| --- | --- |
| `Could not open COM...` | Close Arduino Serial Monitor and confirm the correct COM port. |
| Camera does not open | Close other apps that may be using the webcam; try `CAMERA_INDEX = 1`. |
| Motors do not move | Check L298N motor power, common ground, and battery charge. |
| Robot moves in the wrong direction | Swap the affected motor's two wires or update the direction code. |

## License

This project is released under the [MIT License](LICENSE).
