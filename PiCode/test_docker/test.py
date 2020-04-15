from picamera import PiCamera
from picamera.exc import PiCameraMMALError
from time import sleep
from io import StringIO
from glob import glob
from os.path import getsize

if __name__ == "__main__":
    tries = 0
    while tries < 5:

        try:
            cam = PiCamera(camera_num=0)
        except PiCameraMMALError:
            # Sometimes happens if something else is hogging the resource
            sleep(10)
            continue
        cam.resolution = (512, 512)
        cam.start_preview()
        sleep(4)
        byte_buffer = StringIO()
        byte_buffer.seek(0)

        cam.start_recording('/home/test.mjpeg', format='mjpeg')
        cam.wait_recording(10)
        cam.stop_recording()
        cam.capture('/home/foo.jpeg')

        cam.stop_preview()
        print("Recording")
        cam.close()
        print(glob("/home/*"))
        print(getsize('home/test.mjpeg'))
        print(getsize('home/foo.jpeg'))
        print(byte_buffer.read())
