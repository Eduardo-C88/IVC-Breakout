import cv2

tracker = cv2.TrackerCSRT_create()

def init_track(frame, bbox):
    if bbox is not None:
        tracker.init(frame, bbox)

def find_object(frame):
    track_ok, bbox = tracker.update(frame)
    if track_ok:
        x, y, w, h = [int(v) for v in bbox]
        cv2.rectangle(img=frame, pt1=(x, y), pt2=(x+w, y+h), color=255, thickness=2)

        center_x = (x + x + w) / 2
        if frame.shape[1] != 0:
            return find_object_direction(center_x, frame)
        else:
            return -1, 0
    else:
        cv2.putText(image=frame,
                    text="Tracking failed",
                    org=(5, 35),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 0, 255),
                    thickness=2)
        return -1, 0

def find_object_direction(center, frame):
    position = center / frame.shape[1]

    # Determine the direction based on position
    if position < 1 / 3:
        return -1  # Contour is closer to 1/3
    elif position > 2 / 3:
        return 1  # Contour is closer to 2/3
    else:
        return None
