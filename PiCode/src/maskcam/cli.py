import click
from maskcam.settings import *
from pathlib import Path
from attentive import quitevent
from json import dumps, JSONDecodeError
from maskcam.common_fns import data_generator, session_with_retry_policy, set_verbosity
from base64 import b64encode
import RPi.GPIO as GPIO
from time import time, sleep
from maskcam.settings import DOOR_OUT_PIN, DOOR_OVERRIDE_BUTTON, OPEN_TIME, DEVICE_NAME
from logging import getLogger
from maskcam.common_fns import session_with_retry_policy, open_door, get_serial_number, Pinger, generate_payload
import pytz
from datetime import datetime
from PIL import Image as PIL_IMAGE
from maskcam.camera import Camera

logger = getLogger(__name__)

GPIO.setmode(GPIO.BOARD)


class ConfigObject:
    def __init__(self):
        pass


config_class = click.make_pass_decorator(ConfigObject, ensure=True)


# todo proper knobs on some of these
@click.group()
@click.option('--camera_number', default=CAMERA_NUMBER(), help=CAMERA_NUMBER.help(), type=int)
@click.option('--camera_invert', default=INVERT_CAMERA(), help=INVERT_CAMERA.help(), type=bool)
@click.option('--device_name', default=DEVICE_NAME(), help=DEVICE_NAME.help(), type=str)
@click.option('--minimum_difference', default=MIN_PERCENTAGE_DIFF(), help=MIN_PERCENTAGE_DIFF.help(), type=int)
@click.option('--api_gateway', default=AWS_API_GATEWAY(), help=AWS_API_GATEWAY.help(), type=str)
@click.option('-v', '--verbose', default=4, count=True, help="Verbosity. More v, more verbose. Eg -vvv")
@click.option('--door_button', default=DOOR_OVERRIDE_BUTTON(), help=DOOR_OVERRIDE_BUTTON.help())
@click.option('--door_pin', default=DOOR_OUT_PIN(), help=DOOR_OUT_PIN.help())
@click.option('--opening_time', default=OPEN_TIME(), help=OPEN_TIME.help())
@config_class
def cli(config, camera_number, camera_invert, device_name, minimum_difference, api_gateway, verbose, door_button,
        door_pin, opening_time):
    GPIO.setup(door_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(door_pin, GPIO.OUT)

    # setup logging
    set_verbosity(verbose)
    # Set up generator
    config.camera = Camera(invert=camera_invert, camera_num=camera_number)
    config.camera.start_polling()
    gen = data_generator(Cam=config.camera, threshold=minimum_difference)
    config.camera_num = camera_number
    config.invert_cam = camera_invert
    config.device_name = device_name
    config.min_diff = minimum_difference
    config.gateway_url = api_gateway
    config.generator = gen
    config.door_pin = door_pin
    config.api_gateway = api_gateway
    config.open_time = opening_time

    callback_fn = lambda x: open_door(config, override=True)
    GPIO.add_event_detect(door_button, GPIO.RISING, callback=callback_fn, bouncetime=1000)


@cli.command("to_stdout")
@config_class
def to_stdout(config, file_path):
    # Friendly debugging command.
    serial = get_serial_number()
    while not quitevent.is_set():
        for image in config.generator:
            with session_with_retry_policy() as Session:
                data = generate_payload(config=config, image=image)
                try:
                    response = Session.post(f"{config.gateway_url}upload", data=dumps(data))
                    print(response.content)
                except Exception as e:
                    logger.warning(f"got error {e} with payload {data} continuing anyway")
                    pass


@cli.command("to_file")
@click.option("--file_path", default="/tmp/data", help="Directory to save predictions to", type=str)
@config_class
def to_file(config, file_path):
    # Friendly debugging command.
    serial = get_serial_number()
    image_int = 0
    file_path = Path(file_path)
    if file_path.is_file():
        raise FileExistsError(f"Inputted directory {file_path.absolute()} is a file")
    if not file_path.exists():
        file_path.mkdir(parents=True)
    while not quitevent.is_set():
        for image in config.generator:
            image_int += 1
            PIL_IMAGE.fromarray(image).save(f'{file_path.absolute()}/{image_int}.jpeg')
            with session_with_retry_policy() as Session:
                data = generate_payload(config=config, image=image)
                try:
                    response = Session.post(f"{config.gateway_url}upload", data=dumps(data))
                    with open(f"{file_path.absolute()}/{image_int}.txt", 'wb') as fp:
                        fp.write(response.content.decode('utf-8'))

                except Exception as e:
                    logger.warning(f"got error {e} with payload {data} continuing anyway")
                    pass


@cli.command("to_aws")
@config_class
def to_aws(config):
    serial = get_serial_number()
    ping = Pinger(gateway_URL=f"{config.gateway_url}ping", device_name=config.device_name)
    ping.start()
    while not quitevent.is_set():
        for image in config.generator:
            # We got an event where the camera was diffed.
            with session_with_retry_policy() as Session:
                # Not strictly correct, not a binary image.
                data = generate_payload(config=config, image=image)
                response = Session.post(f"{config.gateway_url}upload", data=dumps(data))
                try:
                    response.raise_for_status()
                except Exception as e:
                    # If we get a non 200 status code, try again
                    logger.debug(e)
                    logger.warning(f"got {response.status_code} \n for payload {data} \n with data {response.content}")
                    continue
                try:
                    response = response.json()
                    if len(response) == 0:
                        logger.info("no people in frame")
                        pass
                    else:
                        if response.get('activity') == 'compliant':
                            logger.info("Opening door. Thanks for wearing a mask.")
                            open_door(config, override=False)
                        else:
                            logger.info(
                                f"I see {len(response['sagemaker_response'])} people and one of you isn't wearing a mask.")
                            logger.info("Wear a mask. I'm not opening the door until you do.")
                            pass
                # If we can't decode this to JSON then it's an invalid payload
                except JSONDecodeError:
                    logger.warning(f"Invalid JSON response from classify \n {response.content}")
                    continue


if __name__ == "__main__":
    cli()
