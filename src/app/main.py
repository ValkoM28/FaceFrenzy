import os
import time
import cv2

from CameraManager import CameraManager
from FaceDetector import FaceDetector
from GameController import GameController, GameState
from HUDRenderer import HUDRenderer

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

ENVIRONMENT = "local"  # "local" | "pynq"


class LocalDisplay:
    def __init__(self):
        pass

    def display_frame(self, frame):
        cv2.imshow("FaceFrenzy", frame)

    def stop(self):
        cv2.destroyAllWindows()


if ENVIRONMENT == "pynq":
    from DisplayManager import DisplayManager
    display = DisplayManager(resolution=(640, 480))
else:
    display = LocalDisplay()

camera = CameraManager(resolution=(640, 480))
detector = FaceDetector(cascade_path='data/haarcascade_frontalface_default.xml')
controller = GameController(face_count_min=1, face_count_max=6, base_countdown=10.0)
hud = HUDRenderer(frame_width=640, frame_height=480)

controller.start_game()
prev_time = time.time()

while True:
    now = time.time()
    dt = now - prev_time
    prev_time = now

    frame = camera.read_frame()
    result = detector.detect(frame)
    annotated = detector.draw_detections(frame, result)

    if controller.state == GameState.CAPTURE:
        controller.submit_face_count(result.face_count)

    controller.update(dt)

    hud_frame = hud.render(annotated, controller)
    display.display_frame(hud_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        controller.toggle_pause()
    elif key == ord('r'):
        controller.reset()
        controller.start_game()

camera.release()
display.stop()
