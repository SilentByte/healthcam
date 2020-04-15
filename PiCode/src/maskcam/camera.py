from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from threading import Thread
from attentive import quitevent
import cv2
import numpy as np
from io import BytesIO
from PIL import Image as PIL_IMAGE
from copy import deepcopy
from base64 import b64encode

class Camera(PiCamera):
    def __init__(self, camera_num: int, invert: bool):
        PiCamera.__init__(self, camera_num=camera_num, resolution=(512, 512))
        if invert:
            self.rotation = 180
        self.framerate = 32
        self.last_image = None
        self.updated = False
        self.stopped = False
        self.__capture_stream = BytesIO()
        self.__capture_stream.seek(0)
        self.__camera_thread = Thread(target=self.__update)

        # Let camera warm up
        time.sleep(1)

    def __update(self):
        # Short circuit on signal or stopped flag.
        while not quitevent.is_set() or not self.stopped:
            # video is lower quality but faster.
            for frame in self.capture_continuous(self.__capture_stream, format='jpeg', use_video_port=True):
                self.last_image = deepcopy(PIL_IMAGE.open(self.__capture_stream))
                self.__capture_stream.seek(0)
                self.updated = True

    def read_frame(self):
        # Only grab an updated frame
        while self.updated:
            self.updated = False
            return self.last_image

    def stop_polling(self):
        self.stopped = True

    def is_stopped(self):
        return not self.__camera_thread.is_alive()

    def start_polling(self):
        self.__camera_thread.start()

    def compare_frames(self, frame1, frame2):
        # convert frames to grayscale to speed up
        if frame1 is not None and frame2 is not None:
            frame1 = np.array(frame1)
            frame2 = np.array(frame2)
        else:
            return 0

        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
        num_pixels = (frame2_gray.shape[0] * frame2_gray.shape[1])
        # to reduce noise pick some small threshold to consider the pixels values "changed"
        # otherwise due to camera noise you get ~80% with no changes
        min_pixel_change = 5
        changed_pixels = np.count_nonzero(cv2.absdiff(frame1_gray, frame2_gray) > min_pixel_change)
        return (changed_pixels / num_pixels) * 100

def image_to_base64(image):
    byte_io = BytesIO()
    byte_io.seek(0)
    image.save(byte_io, 'jpeg')
    image_str = b64encode(byte_io.getvalue()).decode('utf-8')
    return image_str