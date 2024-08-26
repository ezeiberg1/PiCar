import cv2
import argparse
import numpy as np
import math
from picamera import PiCamera
import picamera.array
import time
from angle_func import getAngle
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

camera = PiCamera()
stream = picamera.array.PiRGBArray(camera)

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=float, default = 10,
                    help = 'Run Time in seconds')
parser.add_argument('--cap', action='store', type=float, default = .5,
                    help = 'Time in between image captures')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
args = parser.parse_args()

PWM_pin = 11
freq = 50
GPIO.setup(PWM_pin, GPIO.OUT)
tim = args.tim
delay = args.cap
time_start = time.time() 
cur_time = time_start
loop_count = 0
delta = 0.3
oldPWM = 7.5
newPWM = 7.5
highCycle = 11
debug = args.debug
lowCycle = 4
angleRange = 120
angle = 0
pwm = GPIO.PWM(PWM_pin, freq)
pwm.start(4)

while time_start+tim > cur_time:
  if time_start + delay*loop_count< cur_time:
    oldPWM = newPWM
    camera.capture(stream, format='bgr', use_video_port=True)
    imgFollow = stream.array
    stream.truncate(0)
    imgFollow = cv2.flip(imgFollow, -1)
    cv2.imwrite('test.png', imgFollow)
    angle = getAngle(imgFollow, debug)
    newPWM = oldPWM + delta * (angle *((highCycle-lowCycle)/angleRange))
    if newPWM <= highCycle and newPWM >= lowCycle:
      pwm.ChangeDutyCycle(newPWM)
    else:
      if newPWM > highCycle:
         newPWM = highCycle
         pwm.ChangeDutyCycle(newPWM)
      else:
         newPWM = lowCycle
         pwm.ChangeDutyCycle(newPWM)
  if args.debug:
    print(f'current time: {cur_time:.3f}\t angle: {angle}\t oldPWM: {oldPWM}\t newPWM: {newPWM}')
  cur_time = time.time()
