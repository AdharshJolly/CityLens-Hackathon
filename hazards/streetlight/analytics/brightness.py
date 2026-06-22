import cv2
import numpy as np

def calculate_brightness(frame, bbox):
    x, y, w, h = map(int, bbox)

    crop = frame[
        max(0, y-h//2):y+h//2,
        max(0, x-w//2):x+w//2
    ]

    if crop.size == 0:
        return 0.0

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    return np.mean(gray) / 255.0
