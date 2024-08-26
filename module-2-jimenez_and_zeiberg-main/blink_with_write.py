  
import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep from time module
import argparse
import time
GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)
pin1 = 11
switch_pin = 5
GPIO.setup(pin1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(switch_pin, GPIO.IN)

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--a', action='store', type=float, default = 10,
                    help = 'Run Time')
parser.add_argument('--b', action='store', type=float, default=1,
                    help='Blinks persecond')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
args = parser.parse_args()
blink_rate = args.b
run_time = args.a
start_time = time.time()
iter_count = 0
with open('data.txt','tw') as data:
    while(time.time()<start_time + run_time):
        iter_count += 1
        GPIO.output(pin1, GPIO.HIGH)
        switch = GPIO.input(switch_pin)
        print(switch)
        data.write(f'{time.time():1.0f}\t{GPIO.input(switch_pin)}\n')
        time.sleep(1/blink_rate)
        GPIO.output(pin1, GPIO.LOW)
#        switch = GPIO.input(switch_pin)
        print(switch)
        data.write(f'{time.time():1.0f}\t{GPIO.input(switch_pin)}\n')
        time.sleep(1/blink_rate)
        if args.debug:
            curr_time = time.time()
            print(f'Current time:{curr_time:1.0f}\tNumber of iterations:{iter_count}')
            time.sleep(1)
GPIO.cleanup()
