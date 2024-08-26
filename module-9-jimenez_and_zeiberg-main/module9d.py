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
parser.add_argument('--tim', action='store', type=float, default = 10,
                    help = 'Run Time in seconds')
parser.add_argument('--cap', action='store', type=float, default = .5,
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
delay = args.cap
time_start = time.time() 
cur_time = time_start
loop_count = 0
delta = 0.5
oldPWM = 0
newPWM = 0
highCycle = 10
debug = args.debug
lowCycle = -10
angleRange = 160
angle = 0
car.set_swivel_servo(0)
sleep(3)

while time_start+tim > cur_time:
  if time_start + delay*loop_count< cur_time:
    oldPWM = newPWM
    camera.capture(stream, format='bgr', use_video_port=True)
    imgFollow = stream.array
    stream.truncate(0)
    #imgFollow = cv2.flip(imgFollow, -1)
    cv2.imwrite('test.png', imgFollow)
    angle = getAngle(imgFollow, debug)
    print(angle)
    newPWM = oldPWM + delta * (angle *((highCycle-lowCycle)/(angleRange)))
    print(newPWM)
    if newPWM <= highCycle and newPWM >= lowCycle:
      car.set_swivel_servo(newPWM)
    else:
      if newPWM > highCycle:
         newPWM = highCycle
         car.set_swivel_servo(newPWM)
      else:
         newPWM = lowCycle
         car.set_swivel_servo(newPWM)
  if args.debug:
    print(f'current time: {cur_time:.3f}\t angle: {angle}\t oldPWM: {oldPWM}\t newPWM: {newPWM}')
  cur_time = time.time()
