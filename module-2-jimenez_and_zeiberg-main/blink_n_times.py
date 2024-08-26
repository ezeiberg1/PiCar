
  
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep from time module
import argparse
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering

  
pin1 = 11
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)   

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--n', action='store', type=float, default = 5,
                    help = 'Num Blinks')
args = parser.parse_args()
tot_blink = args.n
ITER_COUNT = 0
while ITER_COUNT < tot_blink: # Run ITER_COUNT times
   ITER_COUNT += 1 # Increment counter
   GPIO.output(pin1, GPIO.HIGH) # Turn on
   sleep(1)                     # Sleep for 1 second
   GPIO.output(pin1, GPIO.LOW)  # Turn off
   sleep(1)                     # Sleep for 1 second
GPIO.cleanup()
