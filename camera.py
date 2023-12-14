import cv2
import tracker

cap = cv2.VideoCapture(0)

def get_cap():
    return cap

def start_camloop():

    if not cap.isOpened():
        cap.open(0)
        _, image = cap.read()
        cv2.imshow("Image", image)
    else:
        ret, image = cap.read()

        if not ret:
            print("Error capturing frame.")

        else:
            image = image[:, ::-1, :]
            cv2.imshow("Image", image)
            #window_size = cv2.getWindowImageRect("Image")
            center = tracker.find_object(image)

            direction = tracker.find_object_direction(center, image.shape[1])

            if direction is not None:
                # Use the 'direction' variable in your code
                if direction == -1:
                    print("Object is closer to 1/3 of the image.")
                elif direction == 1:
                    print("Object is closer to 2/3 of the image.")

            return direction