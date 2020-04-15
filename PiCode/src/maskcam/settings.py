from knobs import Knob
from socket import gethostname


# Knobs are basically wrappers for os.getenvs that have some niceties


CAMERA_NUMBER = Knob(env_name="CAMERA_NUMBER", default=0,
                     description="Raspberry Pi camera number according to "
                                 "https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera")

INVERT_CAMERA = Knob(env_name="CAMERA_INVERT", default=True, description="Vertical invert camera")

DEVICE_NAME = Knob(env_name="DEVICE_NAME", default=gethostname(), description="Device Name")

AWS_REGION = Knob(env_name="AWS_REGION", default='us-east=1', description="AWS region that your resources live in")
MODEL_ENDPOINT_NAME = Knob(env_name="AWS_MODEL_ENDPOINT_NAME", default=False,
                           description="AWS Model endpoint for CVEDIA Human Detector")

AWS_API_GATEWAY = Knob(env_name="AWS_API_GATEWAY", default="https://m5k4jhx1ka.execute-api.us-east-1.amazonaws.com/dev/", description="AWS API Gateway Endpoint")

MIN_PERCENTAGE_DIFF = Knob(env_name="MIN_PERCENTAGE_DIFF", default=50,
                           description="Minimum difference between frames to send")
PERSON_PERCENTAGE = Knob(env_name="PERSON_PERCENTAGE", default=10,
                         description="Minimum probability to consider it being a person")

NO_MASK_THRESHOLD = Knob(env_name="NO_MASK_THRESHOLD", default=50, description="Minimum threshold to measure no mask.")

OPEN_TIME = Knob(env_name="OPEN_TIME", default=5, description="Time to open door in seconds.")

DOOR_OUT_PIN = Knob(env_name="DOOR_OUT_PIN", default=35, description="Pin the door latch is connected to")

DOOR_OVERRIDE_BUTTON = Knob(env_name="DOOR_OVERRIDE_BUTTON", default=37,
                            description="Pin that the override button is connected to")
