# Run with docker run --device "/dev/gpiomem:/dev/gpiomem" foo:ba
FROM resin/raspberry-pi-python:3
LABEL maintainer = "Stephen Mott"
LABEL description = "Minimal code to test whether picam works or not."
RUN READTHEDOCS=True
RUN pip3 install picamera
# to stop complaints about picam
ENV READTHEDOCS True
ENV INITSYSTEM off
RUN apt-get update && apt-get install python-picamera python3-picamera libopenjp2-7 libtiff5 -y
RUN pip3 install picamera RPI.GPIO
RUN usermod -a -G video root
ADD test.py test.py
ENTRYPOINT ["python3", "test.py"]