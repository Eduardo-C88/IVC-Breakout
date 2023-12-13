import cv2
# pip install opencv-contrib-python
import os
import time
import numpy as np

cap = cv2.VideoCapture(0)

def get_cap():
    return cap

tracker = cv2.TrackerCSRT_create()

x, y, w, h = 200, 100, 200, 240
bbox = (x, y, w, h)

_, frame = cap.read()

img = cv2.rectangle(img=frame, pt1=(x, y), pt2=(x+w, y+h), color=255, thickness=2)

cv2.imshow("Image", img)
cv2.waitKey()
tracker.init(frame, bbox)

def find_object(image):
    ret, frame = cap.read()
    center_x = (image.shape[1] / 2)

    if ret:

        track_ok, bbox = tracker.update(frame)
        if track_ok:
            x, y, w, h = bbox
            center_x = (int(x) + int(x + w)) / 2
            image_show = cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=255, thickness=2)
        else:
            image_show = frame.copy()
            cv2.putText(img=image_show,
                        text="Tracking failed",
                        org=(5, 35),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(0, 0, 255),
                        thickness=2)
        cv2.imshow(winname="Image", mat=image_show)

    return center_x
def find_object_direction(center, image_width):
    # Calculate the position relative to the image width
    position = center / image_width

    # Determine the direction based on position
    if position < 1 / 3:
        return -1  # Contour is closer to 1/3
    elif position > 2 / 3:
        return 1  # Contour is closer to 2/3
    else:
        return None
