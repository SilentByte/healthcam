# Set up Pi
[Download Raspbian Buster lite](https://downloads.raspberrypi.org/raspbian_lite_latest) and extract it

Use [Etcher](https://www.balena.io/etcher/) to install the Rasbpian ISO to your SD Card.

On your SD card go to ```boot``` and add a new file called ```ssh```. This will enable SSH on boot.


You should now be able to put your SD card 

Check that your raspberry Pi is online with ```ping raspberrypi.local```
```
PING raspberrypi.local (192.168.0.167) 56(84) bytes of data.
64 bytes from raspberrypi.modem (192.168.0.167): icmp_seq=1 ttl=64 time=0.889 m
```

SSH into the Raspberry Pi

```
# Enable GPIO and Camera
sudo apt-get update
sudo apt-get install pigpio -y
sudo raspi-config nonint do_camera 1
sudo raspi-config nonint do_rgpio 1
# Install docker
sudo apt install docker docker-compose -y
# Setup docker group for current user and green grass user
sudo adduser -m ggc_user
sudo addgroup --system ggc_group
sudo groupadd docker
sudo usermod -aG docker pi
sudo usermod -aG docker ggc_user
# setup opencv (for devel purposes).
sudo apt install libtiff-dev libjpeg8-dev libpng12-dev build-essential  -y
sudo apt install python3-pyqt5 libqtgui4 libjasper-dev libatlas-base-dev libatlas-base-dev libgtk2.0-dev libtbb-dev qt5-default -y
sudo apt install python3-opencv -y
```

Install the MaskCam package
```
git clone git@github.com:SilentByte/healthcam.git
cd healthcam/Picode
pip3 install -r requirements.txt
pip3 install -e .
```
You should now be able to run ```MaskCam``` to access settings 
```zsh
pi@raspberrypi:~ $ MaskCam --help
Usage: MaskCam [OPTIONS] COMMAND [ARGS]...

Options:
  --camera_number INTEGER       Raspberry Pi camera number according to https:
                                //picamera.readthedocs.io/en/release-1.13/api_
                                camera.html#picamera, Default: 0

  --camera_invert BOOLEAN       Vertical invert camera, Default: True
  --device_name TEXT            Device Name, Default: raspberrypi
  --minimum_difference INTEGER  Minimum difference between frames to send,
                                Default: 50

  --api_gateway TEXT            AWS API Gateway Endpoint, Default:
                                https://m5k4jhx1ka.execute-api.us-
                                east-1.amazonaws.com/dev/

  -v, --verbose                 Verbosity. More v, more verbose. Eg -vvv
  --door_button INTEGER         Pin that the override button is connected to,
                                Default: 37

  --door_pin INTEGER            Pin the door latch is connected to, Default:
                                35

  --opening_time INTEGER        Time to open door in seconds., Default: 5
  --help                        Show this message and exit.

Commands:
  to_aws
  to_file
  to_stdout
```
For most cases if you run ```MaskCam --api_gateway {YOUR GATWAY URL} to_aws``` you should be fine.


#Setup Greengrass
# Setup Roles
## Bootstrap Role
Create the "Bootstrap" role which will install your greengrass components onto your raspberry pi.


get your ARN with ```aws iam get-role --role-name Greengrass_ServiceRole ```
```
aws greengrass associate-service-role-to-account --role-arn {YOUR_ROLE} --region us-east-1


```
Create a "boostrap" user that will be creating your greengrass core deployment
```
aws iam create-user --user-name bootstrapuser
aws iam create-access-key --user-name bootstrapuser
aws iam attach-user-policy --user-name bootstrapuser --policy-arn arn:aws:iam::aws:policy/AWSGreengrassFullAccess
aws iam attach-user-policy --user-name bootstrapuser --policy-arn arn:aws:iam::aws:policy/AWSIoTConfigAccess
aws iam attach-user-policy --user-name bootstrapuser --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
```

## Greengrass Service Role
Create your Greengrass Service Role to allow your greengrass group to run.
Check if you have a previous service role
```
aws greengrass get-service-role-for-account --region us-east-1
```
Diasassociate it
```
aws greengrass disassociate-service-role-from-account --region region
```
Give your role the required permissions
```
aws iam create-role --role-name Greengrass_ServiceRole --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "greengrass.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}'
aws iam attach-role-policy --role-name Greengrass_ServiceRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSGreengrassResourceAccessRolePolicy
```
Download greengrass setup
```
wget -q -O ./gg-device-setup-latest.sh https://d1onfpft10uf5o.cloudfront.net/greengrass-device-setup/downloads/gg-device-setup-latest.sh && chmod +x ./gg-device-setup-latest.sh
```
Input the aws-access-key-id and aws-secret-access-key from ```aws iam create-access-key --user-name bootstrapuser```. This will createa a group-name and core-name with the serial number of your raspberry pi.
```
sudo ./gg-device-setup-latest.sh bootstrap-greengrass \
--aws-access-key-id {} \
--aws-secret-access-key {} \
--region us-east-1 \
--group-name $(cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2) \
--core-name $(cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2)

```

```
[GreengrassDeviceSetup] A reboot is required to make cgroups configuration change effective.
You must reboot your device manually and then restart GreengrassDeviceSetup.
```

```sudo reboot```
re run the previous ```./gg-device-setup-latest.sh``` command. This time you'll get
```
Do you want to reuse the configuration from your previous session? Enter 'yes' to reuse the configuration or 'no' to restart the installation.
```
yes

```
You can now use AWS IoT Console to manage your Greengrass group.
```

attach the service role to your docker

```
aws greengrass list-groups
```
get your group name and attach your service role with it
```
get your ARN with ```aws iam get-role --role-name Greengrass_ServiceRole ```
```
Associate this role with your greengrass group
```
aws greengrass associate-role-to-group --group-id {YOUR_GROUP_ID} --role-arn {YOUR_ROLE_ARN}
```
Confirm with
```
aws greengrass get-associated-role --group-id {YOUR_GROUP_ID}
```

# Deploy your container
Replace YOUR_BUCKET_NAME and YOUR_DOCKER_COMPOSE_FILE_NAME with what you created in step 1.
```
aws greengrass create-connector-definition --name MyGreengrassConnectors --initial-version '{
    "Connectors": [
        {
            "Id": "MyDockerAppplicationDeploymentConnector",
            "ConnectorArn": "arn:aws:greengrass:region::/connectors/DockerApplicationDeployment/versions/2",
            "Parameters": {
                "DockerComposeFileS3Bucket": "{YOUR_BUCKET_NAME}",
                "DockerComposeFileS3Key": "{YOUR_DOCKER_COMPOSE_FILE_NAME}",
                "DockerComposeFileDestinationPath": "/home/ggc_user",
                "ForceDeploy": "True"
            }
        }
    ]
}'
```
you should now be able to create a new deployment via the AWS console

# References
[Enable SSH on boot](https://www.raspberrypi.org/forums/viewtopic.php?t=129727)

[raspi-config noint commands](https://github.com/l10n-tw/rc_gui/blob/master/src/rc_gui.c#L50-L100)

[Greengrass quick setup](https://docs.aws.amazon.com/greengrass/latest/developerguide/quick-start.html)

[Connector](https://docs.aws.amazon.com/greengrass/latest/developerguide/docker-app-connector.html)
[Install OpenCV4](https://www.learnopencv.com/install-opencv-4-on-raspberry-pi/)