import os
import time
import cv2

from CameraManager import CameraManager
from FaceDetector import FaceDetector
from GameController import GameController, GameState
from HUDRenderer import HUDRenderer
from LocalDisplayManager import LocalDisplayManager
from ButtonManager import ButtonManager, LocalButtonManager

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

ENVIRONMENT = "local"  # "local" | "pynq"



if ENVIRONMENT == "pynq":
    from pynq.overlays.base import BaseOverlay
    base = BaseOverlay("base.bit")
    buttons = ButtonManager(base)

    from DisplayManager import DisplayManager
    display = DisplayManager(resolution=(640, 480))
else:
    display = LocalDisplayManager(resolution=(640, 480))
    buttons = LocalButtonManager()

camera = CameraManager(resolution=(640, 480))
detector = FaceDetector(cascade_path=cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
controller = GameController(face_count_min=1, face_count_max=6, base_countdown=10.0)
hud = HUDRenderer(frame_width=640, frame_height=480)


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
    buttons.update(key)
    pressed = buttons.read_pressed()

    if key == ord('q'):
        break

    if controller.state == GameState.SETUP:
        if pressed['btn0']:
            controller.dec_max_faces()
        if pressed['btn1']:
            controller.inc_max_faces()
        if pressed['btn2'] or key in (13, 32):  # btn2, Enter, or Space
            controller.confirm_setup()
    elif key == ord('p'):
        controller.toggle_pause()
    elif key == ord('r'):
        controller.reset()
        controller.start_game()

camera.release()
display.stop()
