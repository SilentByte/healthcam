# Setup Docker Compose file
aws s3 mb s3://some_unique_name_that_you_choose --region us-east-1

# Setup Roles
## Bootstrap Role
Create the "Bootstrap" role which will install your greengrass components onto your raspberry pi.


get your ARN with ```aws iam get-role --role-name Greengrass_ServiceRole ```
```
aws greengrass associate-service-role-to-account --role-arn {YOUR_ROLE} --region us-east-1
```
aws iam create-user --user-name bootstrapuser
aws iam create-access-key --user-name bootstrapuser

```
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

SSH into the raSuccessfullyspberry pi

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
sudo apt install python3-pyqt5 libqtgui4 libjasper-dev libatlas-base-dev -y
sudo apt install python3-opencv -y

# Download greengrass setup
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

attach the servie role to your docker

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


aws greengrass create-deployment --deployment-type NewDeployment --group_id {YOUR_GROUP_ID}
```
get your group version id with ```aws greengrass list-groups --query "reverse(sort_by(Groups, &CreationTimestamp))[0]""```
using your group version id (shown as ```LatestVersion``) deploy this
```
aws greengrass create-deployment \
--deployment-type NewDeployment \
--group-id {YOUR_GROUP_ID}
--group-version-id {YOUR_GROUP_VERSION_ID}
```
You should be able to log into your greengrass consol



You shou
##TODO
1. .env file
2. Preload image


# References
[Enable SSH on boot](https://www.raspberrypi.org/forums/viewtopic.php?t=129727)

[raspi-config noint commands](https://github.com/l10n-tw/rc_gui/blob/master/src/rc_gui.c#L50-L100)

[Greengrass quick setup](https://docs.aws.amazon.com/greengrass/latest/developerguide/quick-start.html)

[Connector](https://docs.aws.amazon.com/greengrass/latest/developerguide/docker-app-connector.html)
