import cv2


class LocalDisplayManager:
    def __init__(self, resolution=(640, 480)):
        self.width, self.height = resolution

    def display_frame(self, frame):
        cv2.imshow("FaceFrenzy", frame)

    def stop(self):
        cv2.destroyAllWindows()
