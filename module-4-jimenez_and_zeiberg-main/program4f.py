import argparse
import smbus			#import SMBus module of I2C
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  
from time import sleep          #import
from mod4_funcs import MPU_Read
from mod4_funcs import MPU_Init 
from mod4_funcs import movingAvg
from mod4_funcs import ultrasonic_read
from mod4_funcs import ultrasonic_init
import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np

TRIG = 7   # define input and output pins
ECHO = 11

ultrasonic_init(TRIG, ECHO)   

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
parser.add_argument('--delay', action='store', type=float, default=100,
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
arrAvgUp = [0] * 1000
arrAvgTurn = [0] *1000
position = 0
accelerationUp = 0
accelerationTurn = 0
arrAllUp = [0]*1000
arrAllTurn = [0]*1000
direction = which_measurement(output)
t_previous = 0
d_previous=0

print (" Reading Data of Gyroscope and Accelerometer")

with open('moveData.txt','w') as data:
    while time_start+tim > cur_time:
      if time_start+delay*loop_count< cur_time:
        accelerationUp = get_value(1)
        accelerationTurn = get_value(4)
        direction = which_measurement(output)
        arrAllUp[position] = accelerationUp
        arrAllTurn[position] = accelerationTurn
        arrAvgUp[position] = movingAvg(arrAllUp, position, 3, 0)
        arrAvgTurn[position] = movingAvg(arrAllTurn, position, 3, 0)
        total_distance = ultrasonic_read(TRIG, ECHO)
        time_end = time.time() 
        time_taken = time_end-time_start
        velocity = (total_distance-d_previous)/(time_taken - t_previous)
        print (f'Distance Away: {total_distance:.2f} cm\t Velocity: {velocity:.2f}cm/s') 
        t_previous = time_taken
        d_previous = total_distance
        loop_count = loop_count+1
        data.write(f'{cur_time - time_start:.2f}\t{accelerationUp:.2f}\t{accelerationTurn:.2f}\t{arrAvgUp[position]:.2f}\t{arrAvgTurn[position]:.2f}\t{total_distance}\t{velocity}\n')
        position = position+1
      if args.debug:
        print (f' {direction}  {acceleration}')
        print(arrAvg[position-1])
      cur_time = time.time()
      
fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)
DEBUG   = False                     # For printing debug statements

time    = [0]*MAXSIZE
accUp = [0]*MAXSIZE
accTurn = [0]*MAXSIZE
vel = [0]*MAXSIZE
dist    = [0]*MAXSIZE
MA_accUp = [0]*MAXSIZE
MA_accTurn = [0]*MAXSIZE

i=0
for dat in data:
    values     = dat.split()          # split on white space
    time[i]    = float(values[0])     # first item in file is time
    accUp[i]    = float(values[1])     # second is the acceleration
    accTurn[i] = float(values[2])
    MA_accUp[i] = float(values[3])    # third is the moving average
    MA_accTurn[i] = float(values[4])
    dist[i] = float(values[5])       # fourth is the distance
    vel[i] = float(values[6])        # fifth is average velocity
    if DEBUG: print (f'{i}\t{time[i]}\t{dist[i]}')
    i = i + 1

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

# Both on one Graph
#plt.plot(time, dist, label="dist")
#plt.plot(time, MA_dist, label="MovAvg")
#plt.grid()                          # show the grid
#plt.xlabel('time - sec')
#plt.ylabel('Distance in CM, Moving Average in CM')
#plt.savefig('distance.png')   




plt.clf()                           # start new plot
plt.figure()
plt.subplot(311)
plt.grid()                          # show the grid
plt.plot(time, dist)
plt.ylabel('Distance in CM')
plt.subplot(312)
plt.plot(time, MA_accUp)
plt.grid()                          # show the grid
plt.ylabel('Up Acc in g')
plt.xlabel('time - sec')
plt.subplot(313)
plt.grid()                          # show the grid
plt.plot(time, MA_accTurn)
plt.ylabel('Turn Acc in g')
plt.savefig("AllQuantities.png")
GPIO.cleanup()
