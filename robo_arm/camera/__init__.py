import cv2
import numpy as np
from PIL import Image, ImageTk

class Camera:
    def __init__(self):
        self.video_device = cv2.VideoCapture(0)
        self.video_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.red_lower = np.array([100 + 50,100,100], dtype='uint8')
        self.red_upper = np.array([255 - 50,255,255], dtype="uint8")

        self.white_lower = np.array([0,0,255 - 50], dtype="uint8")
        self.white_upper = np.array([255,50,255], dtype="uint8")

    def read(self):
        _, frame = self.video_device.read()
        return frame

    def tk_image(self, array):
        from_array_image = Image.fromarray(array)
        return ImageTk.PhotoImage(image=from_array_image)

    def detected_colors_in_frame(self, frame):
        found_colors = []

        # red
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        image = Image.fromarray(mask)
        bbox = image.getbbox()
        if bbox is not None:
            found_colors.append('red')

        # white
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.white_lower, self.white_upper)
        image = Image.fromarray(mask)
        bbox = image.getbbox()
        if bbox is not None:
            found_colors.append('white')

        return found_colors

    def __del__(self):
        self.video_device.release()

