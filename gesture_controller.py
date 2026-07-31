"""Send hand-gesture commands from the detector to an Arduino robot."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import serial


# Arduino serial configuration
SERIAL_PORT = "COM14"
BAUD_RATE = 9600

# The detector is kept beside this file so it also works when run from another folder.
DETECTOR_SCRIPT = Path(__file__).with_name("hand_gesture_detector.py")


def command_for_finger_count(finger_count: int) -> str:
    """Convert a detected finger count into the Arduino command character."""
    commands = {
        0: "0",  # Stop
        1: "1",  # Forward
        2: "2",  # Backward
        3: "3",  # Turn right
        4: "4",  # Turn left
    }
    return commands.get(finger_count, "5")  # Honk for five fingers


def main() -> None:
    if not DETECTOR_SCRIPT.is_file():
        print(f"ERROR: Cannot find detector script: {DETECTOR_SCRIPT.name}")
        sys.exit(1)

    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as error:
        print(f"ERROR: Cannot open {SERIAL_PORT}: {error}")
        print("Check the Arduino connection, COM port, and Serial Monitor.")
        sys.exit(1)

    print(f"Connected to Arduino on {SERIAL_PORT}.")
    time.sleep(3)  # Most Arduino boards reset after the serial connection opens.

    detector = subprocess.Popen(
        [sys.executable, str(DETECTOR_SCRIPT)],
        stdout=subprocess.PIPE,
        text=True,
        bufsize=1,
        # Keep detector errors visible instead of filling an unread error pipe.
        stderr=None,
    )
    print("Gesture detector started. Press Q in the camera window to quit.")

    last_command: str | None = None

    try:
        assert detector.stdout is not None
        for line in detector.stdout:
            try:
                finger_count = int(line.strip())
            except ValueError:
                continue  # Ignore any non-numeric diagnostic output.

            command = command_for_finger_count(finger_count)
            if command != last_command:
                ser.write(command.encode("ascii"))
                print(f"Fingers: {finger_count} -> Arduino command: {command}")
                last_command = command

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if detector.poll() is None:
            detector.terminate()
            try:
                detector.wait(timeout=3)
            except subprocess.TimeoutExpired:
                detector.kill()
                detector.wait()

        if ser.is_open:
            ser.write(b"0")  # Always stop the robot before closing the port.
            ser.close()
        print("Robot stopped and serial connection closed.")


if __name__ == "__main__":
    main()
