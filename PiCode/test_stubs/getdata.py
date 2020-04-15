# Test function for docker container to check that pi is set up properly

from picamera import PiCamera
from time import sleep
if __name__ == "__main__":
    sleep(1)
    cam = PiCamera(camera_num=0)
    sleep(1)
    cam.resolution = (512, 512)
    cam.start_preview()
    sleep(1)
    cam.start_recording('test.mjpeg')
    cam.wait_recording(5)
    cam.stop_recording()
    sleep(1)
    cam.capture('foo.jpeg')
    cam.stop_preview()
