# Test for docker GPIO
# I dont care what the values actually are
# I just need to make sure it doesn't crash out
# Run on a pi with -device /dev/gpiomem:/dev/gpiomem
import Rpi.GPIO as GPIO
from time import sleep
HIGH_IN = 40
LOW_IN = 37
OUT_PIN = 33

import RPi.GPIO as GPIO
from time import sleep
HIGH_IN = 40
LOW_IN = 37
OUT_PIN = 33

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    sleep(1)
    GPIO.setup(OUT_PIN, GPIO.OUT)
    GPIO.setup(LOW_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(HIGH_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    sleep(1)
    print(f"High input is {GPIO.input(HIGH_IN)}")
    print(f"Low input is {GPIO.input(LOW_IN)}")
    print("Trying output")
    GPIO.output(OUT_PIN, GPIO.HIGH)
    sleep(5)
    GPIO.output(OUT_PIN, GPIO.LOW)
    sleep(1)
    print("Looks good to me")
    GPIO.cleanup()
    exit()
