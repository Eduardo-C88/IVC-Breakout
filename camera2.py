import cv2
import tracker2

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
            direction = tracker2.find_object(img2)
        else:
            isInit = True
            tracker2.init_track(img2, (280, 100, 100, 100))

        if direction is not None:
            # Use the 'direction' variable in your code
            if direction == -1:
                print("Object is closer to 1/3 of the image.")
            elif direction == 1:
                print("Object is closer to 2/3 of the image.")
        cv2.imshow("Image", img2)
        return direction