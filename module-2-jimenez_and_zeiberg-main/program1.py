  
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep from time module
import argparse
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)

pin1 = 11
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)
ITER_COUNT = 15
  

while ITER_COUNT > 0:
    GPIO.output(pin1, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin1, GPIO.LOW)
    sleep(1)
    ITER_COUNT -= 1
GPIO.cleanup()