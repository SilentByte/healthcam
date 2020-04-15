import os
import glob
import json
import boto3
import sagemaker

if __name__ == "__main__":
    from base64 import b64encode, b64decode

    with open('data/lotsofpeople.jpg', 'rb') as fp:
        image_data = fp.read()
    # basically just a sanity check since we do encode/decode as b64
    image_data = b64encode(image_data).decode('utf-8')
    image_decoded = b64decode(image_data)

    sagemaker = boto3.client(
        'runtime.sagemaker',
        region_name='us-east-1'
    )

    result = sagemaker.invoke_endpoint(
        EndpointName="myendpoin3123t-name132",
        ContentType='image/jpeg',
        Body=bytearray(image_decoded))
    output = result['Body'].read()
    # output looks like data/responses.py