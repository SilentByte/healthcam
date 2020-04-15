import requests
from base64 import b64encode
from datetime import datetime
from json import dumps

if __name__ == "__main__":
    config = object()
    config.gateway_url = "1234"
    with open('data/penguin.png','rb') as fp:
        image_data = fp.read()
    image_data = b64encode(image_data).decode('utf-8')

    data = dict(image=image_data, runtime=1234, device_name="DEVICE_NAME",
                person_threshold=0.532, mask_treshhold=0.5432)
    requests.post(f"{config.gateway_url}/classify", data=dumps(data))