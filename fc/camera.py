from picamera.array import PiRGBArray
from picamera import PiCamera
import time


class MyCamera:
    my_camera = PiCamera()

    def __init__(self, width, height):
        #  Initialize the camera and grab a reference to the raw camera capture

        frame_width = int(width / 2)
        frame_height = height

        self.my_camera.vflip = True
        self.my_camera.hflip = True
        self.my_camera.resolution = (frame_width, frame_height)
        self.my_camera.framerate = 42

        #  Allow the camera to warm-up
        time.sleep(0.1)


class RawCapture:
    rawCapture = None

    def __init__(self, camera, width, height):
        self.rawCapture = PiRGBArray(camera, size=(int(width / 2), height))
