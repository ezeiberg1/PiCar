import argparse
import smbus
import time			#import SMBus module of I2C
from time import sleep          #import
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards

MPU_Init(bus)

def get_value(output):
  value = MPU_Read(bus, output)
  return value

def which_measurement (output):
  if output == 1:
    measurement = 'Ax'
  elif output == 2:
    measurement = 'Ay'
  elif output == 3:
    measurement = 'Az'
  elif output == 4:
    measurement = 'Gx'
  elif output == 5:
    measurement = 'Gy'
  else:
    measurement = 'Gz'
  return measurement

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=float, default = 5,
                    help = 'Run Time in seconds')
parser.add_argument('--delay', action='store', type=float, default=0.1,
                    help='Time in between readings in milliseconds')
parser.add_argument('--output', action='store', type=float, default=1,
                    help='Which measurement to display (1-6)')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
args = parser.parse_args()
tim = args.tim
output = args.output
delay = args.delay * .001

time.sleep(.5)              # let the sensor initialize
time_start = time.time()
cur_time = time_start
loop_count = 0

print (" Reading Data of Gyroscope and Accelerometer")

while time_start+tim > cur_time:
  if time_start + delay*loop_count< cur_time:
    acceleration = get_value(output)
    direction = which_measurement(output)
    print (f' {direction}  {acceleration}') 
  if args.debug:
      print (f' {direction}  {acceleration}')
  loop_count = loop_count +1
  cur_time = time.time()
  sleep(0.1)
