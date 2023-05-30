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

    def detected_colors(self):
        found_colors = []
        frame = self.read()

        # red
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.red_lower, self.red_upper)
        image = Image.fromarray(mask)
        bbox = image.getbbox()
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            length = abs(x2 - x1)
            height = abs(y2 - y1)
            if length >= 40 and height >= 40:
                found_colors.append('Kırmızı')

        # white
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.white_lower, self.white_upper)
        image = Image.fromarray(mask)
        bbox = image.getbbox()
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            length = abs(x2 - x1)
            height = abs(y2 - y1)
            if length >= 40 and height >= 40:
                found_colors.append('Beyaz')

        return found_colors

    def __del__(self):
        self.video_device.release()

