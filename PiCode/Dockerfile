FROM resin/raspberry-pi-python:3
LABEL maintainer = "Stephen Mott"
LABEL description = "Minimal code to test whether picam works or not."
RUN READTHEDOCS=True
RUN pip3 install picamera
# to stop complaints about picam
ENV READTHEDOCS True
ENV INITSYSTEM off
RUN apt-get update && apt-get install python-picamera python3-picamera libopenjp2-7 libtiff5 python-rpi.gpio python3-rpi.gpio -y
RUN pip3 install picamera
RUN usermod -a -G video root
ADD test.py test.py
COPY src src
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY readme.md readme.md
ENTRYPOINT ["MaskCam", "to_aws"]