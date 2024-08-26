import cv2
from picar import PiCar
import argparse
import numpy as np
import math
from picamera import PiCamera
import picamera.array
import time
from angle_func import getAngle
from time import sleep
camera = PiCamera()
stream = picamera.array.PiRGBArray(camera)

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=float, default = 20,
                    help = 'Run Time in seconds')
parser.add_argument('--cap', action='store', type=float, default = .04,
                    help = 'Time in between image captures')
parser.add_argument('--vel', action='store', type=float, default = .05,
                    help = 'Time in between image captures')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
parser.add_argument('--mock_car', action='store_true', 
                    help='If not present, run on car, otherwise mock hardware')
args = parser.parse_args()

car = PiCar(mock_car=args.mock_car)
#car.configure_swivel_servo_positions(4, 7, 11)
freq = 50
tim = args.tim
capDelay = args.cap
velDelay = args.vel
time_start = time.time() 
cur_time = time_start
speed_count = 0
angle_count = 0
delta = 0.3
oldPWM = 0
newPWM = 0
highCycle = 10
debug = args.debug
lowCycle = -10
angleRange = 160
angle = 0
distance = 0
car.set_steer_servo(0)
car.set_nod_servo(-2)
car.set_motor(80)
sleep(.3)

while time_start+tim > cur_time:
  if time_start + velDelay*speed_count< cur_time:
    distance  = car.read_distance()
#    print(f'distance {distance}')
    if distance < 20:
      #print('<10')
      car.set_motor(0)
    elif distance < 30:
      car.set_motor(25)
    elif distance < 100:
      newSpeed = distance * .2 + 25
      car.set_motor(newSpeed)
      delta = .1
    elif distance < 300:
      car.set_motor(60)
      delta = .1
      #print('>50')
    else:
      car.set_motor(80)
      delta = .15
    speed_count = speed_count + 1
  if time_start + capDelay*angle_count< cur_time:
    oldPWM = newPWM
    camera.capture(stream, format='bgr', use_video_port=True)
    imgFollow = stream.array
    stream.truncate(0)
    #imgFollow = cv2.flip(imgFollow, -1)
    cv2.imwrite('test.png', imgFollow)
    angle = getAngle(imgFollow)
 #   print(angle)
    newPWM = oldPWM + delta * (abs(angle) *((highCycle-lowCycle)/(angleRange)))
    if angle < 0:
      newPWM = -newPWM
 #   print(f'pwm: {newPWM}')
    if newPWM <= highCycle and newPWM >= lowCycle:
      #if angle<10:
       #  car.set_steer_servo(0)
      #else:
         car.set_steer_servo(newPWM)
    else:
      if newPWM > highCycle:
         newPWM = highCycle
         car.set_steer_servo(newPWM)
      else:
         newPWM = lowCycle
         car.set_steer_servo(newPWM)
    angle_count = angle_count + 1
  if args.debug:
    print(f'current time: {cur_time:.3f}\t angle: {angle}\t oldPWM: {oldPWM}\t newPWM: {newPWM} \t distance: {distance}')
  cur_time = time.time()
