from maskcam.camera import Camera, image_to_base64
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests import Session
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import basicConfig, getLogger
import RPi.GPIO as GPIO
from json import dumps
from time import sleep
from attentive import quitevent
from threading import Thread
from base64 import b64encode
import pytz
from datetime import datetime
from .settings import NO_MASK_THRESHOLD, PERSON_PERCENTAGE

logger = getLogger(__name__)


def get_serial_number():
    # Get the rpis serial number
    try:
        with open('/proc/cpuinfo', 'r') as fp:
            for line in fp:
                if line[0:6] == "Serial":
                    cpuserial = line[10:26]
                    return cpuserial
    except:
        cpuserial = "ERROR000000000"
        return cpuserial


serial = get_serial_number()


def generate_payload(config, image, override='False'):
    data = dict(photo_data=image_to_base64(image),
                timestamp=datetime.utcnow().replace(tzinfo=pytz.utc).isoformat(),
                person_threshold=PERSON_PERCENTAGE(), mask_threshold=100 - NO_MASK_THRESHOLD(),
                device_serial=serial, override=override)
    return data


class Pinger():
    def __init__(self, gateway_URL, device_name):
        self.__stop = False
        self.gateway_url = gateway_URL
        self.session = session_with_retry_policy()
        self.thread = Thread(target=self.continue_until_stopped)
        self.serial = get_serial_number()
        self.device_name = device_name

    def stop(self):
        self.__stop = True

    def continue_until_stopped(self):
        while not quitevent.is_set():
            if self.__stop:
                break
            try:
                self.session.post(self.gateway_url,
                                  data=dumps(dict(device_serial=self.serial, device_name=self.device_name)))
                sleep(30)
            except Exception as e:
                logger.debug(f"Error code {e} while pinging")
                sleep(30)

    def start(self):
        self.thread.start()


def data_generator(Cam, threshold):
    images = []
    last_image = 0
    with Cam:
        # start getting images in a background thread
        # pre fill array
        images.append(Cam.read_frame())
        images.append(Cam.read_frame())
        # While we don't sigkill

        while not quitevent.is_set():
            if Cam.updated:
                images[last_image] = Cam.read_frame()
                # Sanity check that we have two images.
                if len(images) > 1:
                    threshold_percentage = Cam.compare_frames(images[0], images[1])
                    if threshold_percentage > threshold:
                        yield images[last_image]
                # rotate frames
                if last_image == 0:
                    last_image = 1
                else:
                    last_image = 0


def session_with_retry_policy() -> Session:
    http = Session()
    retry_strategy = Retry(
        total=5,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=["POST"],
        backoff_factor=3
    )
    adaptor = HTTPAdapter(max_retries=retry_strategy)
    http.adapters = {"https://": adaptor, "http://": adaptor}
    return http


def set_verbosity(verbose: int):
    log_int = {'4': DEBUG, '3': INFO, '2': WARNING, '1': ERROR, '0': CRITICAL}
    # The most verbose you can go is debug
    if verbose > len(log_int):
        basicConfig(level=DEBUG)
    else:
        if str(verbose) not in log_int.keys():
            raise ValueError(f"Invalid log level {verbose}")
        basicConfig(level=log_int[str(verbose)])
    # get some chatty logs to chill for a bit.
    getLogger("PIL").setLevel(WARNING)
    getLogger("boto3").setLevel(WARNING)
    # URLLIB gets way too chatty
    if verbose > 4:
        getLogger("urllib3").setLevel(DEBUG)
    else:
        getLogger("urllib3").setLevel(INFO)


def open_door(config, override=False):
    if override:
        logger.debug("Door triggered over by override. Uploading")
    pin = config.door_pin
    open_time = config.open_time

    GPIO.output(pin, 1)
    sleep(open_time)
    logger.debug(f"Door closing")
    GPIO.output(pin, 0)
    # if its an override we also need to send image.
    if override:
        with session_with_retry_policy() as Session:
            try:
                image = None
                while image is None:
                    image = config.camera.read_frame()

                data = dumps(generate_payload(config, image, override="True"))
                response = Session.post(url=f"{config.api_gateway}/upload",
                             data=data)
                logger.debug(response.json())
            except Exception as e:
                logger.debug(e)
                logger.warning(f"Something went wrong when trying to send override {pin}. Check debug log.")