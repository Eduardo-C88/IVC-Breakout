import cv2
import tracker

cap = cv2.VideoCapture(0)
cap.open(0)
isInit = False
direction = None

def get_cap():
    return cap

def start_camloop():
    global isInit
    global direction
    ret, image = cap.read()

    if not ret:
        print("Error capturing frame.")

    else:
        img2 = image[:, ::-1, :].copy()

        if isInit:
            direction = tracker.find_object(img2)
        else:
            isInit = True
            tracker.init_track(img2, (300, 180, 100, 100))

        if direction is not None:
            # Use the 'direction' variable in your code
            if direction == -1:
                print("Object is closer to 1/3 of the image.")
            elif direction == 1:
                print("Object is closer to 2/3 of the image.")
        cv2.imshow("Image", img2)
        return direction