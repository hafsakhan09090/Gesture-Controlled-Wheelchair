"""Count raised fingers with MediaPipe and print the count for the controller."""

from __future__ import annotations

import sys
import time

import cv2
import mediapipe as mp


CAMERA_INDEX = 0
FRAME_WIDTH = 1040
FRAME_HEIGHT = 880

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COMMAND_LABELS = [
    "0 - STOP",
    "1 - FORWARD",
    "2 - BACKWARD",
    "3 - TURN RIGHT",
    "4 - TURN LEFT",
    "5 - HONK",
]


def count_raised_fingers(landmarks, handedness: str) -> int:
    """Return the number of raised fingers for one detected hand."""
    fingers_up = 0

    # Thumb direction depends on whether the detected hand is left or right.
    thumb_tip_x = landmarks[4].x
    thumb_joint_x = landmarks[3].x
    if (handedness == "Right" and thumb_tip_x < thumb_joint_x) or (
        handedness == "Left" and thumb_tip_x > thumb_joint_x
    ):
        fingers_up += 1

    # For the four remaining fingers, an extended fingertip is above its joint.
    for tip_id, joint_id in ((8, 6), (12, 10), (16, 14), (20, 18)):
        if landmarks[tip_id].y < landmarks[joint_id].y:
            fingers_up += 1

    return fingers_up


def main() -> None:
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("ERROR: Could not open webcam.", file=sys.stderr)
        sys.exit(1)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    mp_hands = mp.solutions.hands
    drawing = mp.solutions.drawing_utils
    previous_time = time.time()

    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
    ) as hands:
        while True:
            success, frame = camera.read()
            if not success:
                continue

            result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            finger_count = 0

            if result.multi_hand_landmarks and result.multi_handedness:
                hand_landmarks = result.multi_hand_landmarks[0]
                handedness = result.multi_handedness[0].classification[0].label
                finger_count = count_raised_fingers(hand_landmarks.landmark, handedness)
                drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # The controller reads only this numeric output from standard output.
            print(finger_count, flush=True)

            cv2.putText(frame, str(finger_count), (35, 250), cv2.FONT_HERSHEY_SIMPLEX,
                        7, WHITE, 5, cv2.LINE_AA)

            current_time = time.time()
            fps = 1 / max(current_time - previous_time, 0.001)
            previous_time = current_time
            cv2.putText(frame, f"FPS: {int(fps)}", (15, 55), cv2.FONT_HERSHEY_SIMPLEX,
                        1, BLACK, 2, cv2.LINE_AA)

            for index, label in enumerate(COMMAND_LABELS):
                cv2.putText(frame, label, (700, 45 + index * 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, WHITE, 2, cv2.LINE_AA)

            cv2.imshow("Hand Gesture Robot Control", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
