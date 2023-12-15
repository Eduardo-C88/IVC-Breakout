import cv2


class Tracker:

    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()

    def init_track(self, frame, bbox):
        if bbox is not None:
            self.tracker.init(frame, bbox)

    def track(self, frame):

        track_ok, (x, y, w, h) = self.tracker.update(frame)
        if track_ok:
            cv2.rectangle(img=frame, pt1=(x, y), pt2=(x + w, y + h), color=(0, 255, 0), thickness=2)

            x = (x + (x + w)) / 2
            position_x = x * 100 / frame.shape[1]

            return self.find_object_direction(position_x)
        else:
            cv2.putText(img=frame,
                        text="Tracking failed",
                        org=(5, 35),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(0, 0, 255),
                        thickness=2)
            return -1, 0

    def find_object_direction(self, center):
        # Calculate the position relative to the image width

        # Determine the direction based on position
        if center < 30:
            return -1  # Contour is closer to 1/3
        elif center > 70:
            return 1  # Contour is closer to 2/3
        else:
            return None
