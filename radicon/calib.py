# encoding=utf-8

import cv2
import numpy as np

# -------------------------------
# ---------- CONSTANTS ----------
# -------------------------------
CORNER = [[177,114], [681,111], [217,342], [632,350]]
SH, SW = 900-45, 1600



# -------------------------------
# ---------- VARIABLES ----------
# -------------------------------



# -----------------------------
# ---------- METHODS ----------
# -----------------------------



# --------------------------
# ---------- MAIN ----------
# --------------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

#"""
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        print(x, y)

while True:
    ret, frame = cap.read()

    cv2.setMouseCallback("cam", mouse_event)
    cv2.imshow("cam", frame)
    cv2.waitKey(0)
#"""

"""
per1 = np.float32(CORNER)
per2 = np.float32([[0,0], [SW,0], [0,SH], [SW,SH]])
m = cv2.getPerspectiveTransform(per1, per2)

while True:
    ret, frame = cap.read()
    screen = cv2.warpPerspective(frame, m, (SW, SH))

    cv2.imshow("cam", screen)
    cv2.waitKey(0)
"""



