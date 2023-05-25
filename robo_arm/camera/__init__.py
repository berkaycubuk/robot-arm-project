import cv2

class Camera:
    def __init__(self):
        self.video_device = cv2.VideoCapture(0)
        self.video_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.video_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def read(self):
        _, frame = self.video_device.read()
        return frame

    def __del__(self):
        self.video_device.release()

