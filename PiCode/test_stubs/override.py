import requests
data = dict(device_name="DEVICE_NAME")

requests.post('https://gateway/overrride',data=data)