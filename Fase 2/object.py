from ultralytics import YOLO
import cv2
import numpy as np

cap = cv2.VideoCapture()
def get_cap():
    return cap

model = YOLO("yolov8n.pt")

cv2.namedWindow("Image")
def find_object_position(image):
    #image = image[:, ::-1, :]
    image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)

    results = model(image)
    image_objects = image.copy()
    center_x = (image.shape[1] / 2)

    objects = results[0]
    for object in objects:
        box = object.boxes.data[0]
        if int(box[5]) == 76:            #76 is scissors
            cv2.rectangle(img=image_objects,
                          pt1=(int(box[0]), int(box[1])),
                          pt2=(int(box[2]), int(box[3])),
                          color=(255, 0, 0),
                          thickness=2)
            center_x = (int(box[0]) + int(box[2])) / 2
            text = "{}:{:.2f}".format(objects.names[int(box[5])], box[4])
            cv2.putText(img=image_objects,
                        text=text,
                        org=np.array(np.round((float(box[0]), float(box[1] - 1))), dtype=int),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(255, 0, 0),
                        thickness=1)
    image_objects = cv2.cvtColor(src=image_objects, code=cv2.COLOR_RGB2BGR)
    cv2.imshow(winname="Image", mat=image_objects)

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
