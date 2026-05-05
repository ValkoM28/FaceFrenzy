from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
import numpy as np
import cv2

class DisplayManager: 
    def __init__(self, resolution=(640, 480)):
        self.base = BaseOverlay("base.bit")
        self.hdmi_out = self.base.video.hdmi_out
        self.width, self.height = resolution
        self.hdmi_out.configure(VideoMode(self.width, self.height, 24), PIXEL_BGR)
        self.hdmi_out.start()


    def display_frame(self, frame):
        outframe = self.hdmi_out.newframe()
        outframe[0:self.height, 0:self.width, :] = frame[0:self.height, 0:self.width, :]
        self.hdmi_out.writeframe(outframe)
    

    def stop(self):
        self.hdmi_out.stop()


