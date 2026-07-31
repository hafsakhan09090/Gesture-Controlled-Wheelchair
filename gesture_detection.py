"""
Gesture Detection Module

Captures webcam video, detects a single hand using MediaPipe,
counts extended fingers, and prints the finger count to stdout.
Designed to be used with a serial controller that reads stdout.
"""

import cv2
import mediapipe as mp
import time
import sys

CAMERA_WIDTH = 1040
CAMERA_HEIGHT = 880

WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(0,0,255)
BLACK=(0,0,0)

GESTURES={0:"STOP",1:"FORWARD",2:"BACKWARD",3:"LEFT",4:"RIGHT",5:"HORN"}

mp_hands=mp.solutions.hands
mp_draw=mp.solutions.drawing_utils

hands=mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to access webcam.")
    sys.exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,CAMERA_HEIGHT)

prev_time=0

def count_fingers(hand):
    pts=[]
    for idx,lm in enumerate(hand.landmark):
        pts.append((idx,int(lm.x*CAMERA_WIDTH),int(lm.y*CAMERA_HEIGHT)))
    fingers=[]
    fingers.append(1 if pts[4][1]>pts[3][1] else 0)
    fingers.append(1 if pts[8][2]<pts[6][2] else 0)
    fingers.append(1 if pts[12][2]<pts[10][2] else 0)
    fingers.append(1 if pts[16][2]<pts[14][2] else 0)
    fingers.append(1 if pts[20][2]<pts[18][2] else 0)
    return sum(fingers)

while True:
    ok,frame=cap.read()
    if not ok:
        continue
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)
    count=0
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
            count=count_fingers(hand)
    print(count,flush=True)
    cv2.putText(frame,f"Fingers: {count}",(20,50),cv2.FONT_HERSHEY_SIMPLEX,1,GREEN,2)
    cv2.putText(frame,f"Command: {GESTURES[count]}",(20,95),cv2.FONT_HERSHEY_SIMPLEX,1,RED,2)
    y=150
    for k,v in GESTURES.items():
        cv2.putText(frame,f"{k} -> {v}",(700,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,WHITE,2)
        y+=35
    now=time.time()
    fps=1/(now-prev_time) if prev_time else 0
    prev_time=now
    cv2.putText(frame,f"FPS: {int(fps)}",(20,140),cv2.FONT_HERSHEY_SIMPLEX,0.8,BLACK,2)
    cv2.imshow("Gesture Detection",frame)
    if cv2.waitKey(1)&0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
