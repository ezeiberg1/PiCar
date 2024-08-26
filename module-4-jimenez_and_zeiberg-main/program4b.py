import argparse
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BOARD)    # Use physical pin numberin
import mod4_funcs  
TRIG = 7   # define input and output pins
ECHO = 11

      # set up the input and output pins
mod4_funcs.ultrasonic_init(TRIG, ECHO)     


parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=float, default = 5,
                    help = 'Run Time in seconds')
parser.add_argument('--delay', action='store', type=float, default=0.1,
                    help='Time in between readings in milliseconds')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
args = parser.parse_args()
tim = args.tim
delay = args.delay * .001

time_start = time.time() 
cur_time = time_start
loop_count = 0
t_previous = 0
d_previous = 0

while time_start+tim > cur_time:
  if time_start + delay*loop_count< cur_time:
    total_distance = mod4_funcs.ultrasonic_read(TRIG, ECHO)
    time_end = time.time() 
    time_taken = time_end-time_start
    velocity = (total_distance-d_previous)/(time_taken - t_previous)
    print (f'Distance Away: {total_distance:.2f} cm\t Velocity: {velocity:.2f}cm/s') 
    t_previous = time_taken
    d_previous = total_distance

    if args.debug:
      print (f'Taken in {time_taken:.3f} seconds')
    loop_count = loop_count+1
  cur_time = time.time()
  
GPIO.cleanup()
