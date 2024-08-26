import argparse
import smbus			#import SMBus module of I2C
import time
from time import sleep          #import
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 
from mod4_funcs import movingAvg

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
parser.add_argument('--tim', action='store', type=int, default = 5,
                    help = 'Run Time in seconds')
parser.add_argument('--delay', action='store', type=float, default=0.1,
                    help='Time in between readings in milliseconds')
parser.add_argument('--output', action='store', type=int, default=1,
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
arrAvg = [0] * 100
position = 0
acceleration = 0
arrAll = [0]*100

print (" Reading Data of Gyroscope and Accelerometer")

with open('data.txt','w') as data:
    while time_start+tim > cur_time:
       acceleration = get_value(output)
       direction = which_measurement(output)
       arrAll[position] = acceleration
       arrAvg[position] = movingAvg(arrAll, position, 3, 0)
       data.write(f'{cur_time - time_start:.2f}\t{acceleration:.2f}\t{arrAvg[position]:.2f}\n')
       position = position + 1
       if args.debug:
         print (f' {direction}  {acceleration}')
         print(arrAvg[position-1])
       loop_count = loop_count+1
       cur_time = time.time()
       sleep(0.1)
