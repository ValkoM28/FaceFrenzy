import cv2

class CameraManager:
    def __init__(self, resolution=(640, 480)):
        self.width, self.height = resolution
        self.video_in = cv2.VideoCapture(0)
        self.video_in.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video_in.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read_frame(self):
        ret, frame = self.video_in.read()
        if not ret:
            raise Exception("Failed to read frame from camera")
        return frame

    def release(self):
        self.video_in.release()