import cv2
import segment

camera_index = 1

cap = cv2.VideoCapture()

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
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = segment.update_segmentation(image_hsv)

            direction = segment.find_countour_direction(mask, image.shape[1])

            if direction is not None:
                # Use the 'direction' variable in your code
                if direction == -1:
                    print("Contour is closer to 1/3 of the image.")
                elif direction == 1:
                    print("Contour is closer to 2/3 of the image.")

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Result", image)
            return direction

            """ Tracking
            center = segment.find_countour_center(mask)
            if center is not None:
                center_x = center[0]

                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                cv2.circle(image, center, 5,(0, 255, 0), -1)
                cv2.imshow("Result", image)
               return center_x"""