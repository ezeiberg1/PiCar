
import argparse
import time			#import SMBus module of I2C
from time import sleep 
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
import mod8_func as motor

GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

parser = argparse.ArgumentParser(description = 'Data for this program')
parser.add_argument('--tim', action='store', type=int, default = 5,
                    help = 'Run Time in seconds')
parser.add_argument('--calc', action='store', type=float, default= 250,
                    help='Time in between calculating speed in milliseconds')
parser.add_argument('--pwm', action='store', type=int, default=50,
                    help='PWM')
parser.add_argument('--sample', action='store', type=int, default=5,
                    help='Time between AD Samples in msec')
parser.add_argument('--delay', action='store', type=int, default=2,
                    help='Time before starting loop')
parser.add_argument('--rps', action='store', type=float, default=4,
                    help='RPS')
parser.add_argument('--kp', action='store', type=float, default=0,
                    help='proportional control constant')
parser.add_argument('--ki', action='store', type=float, default=0,
                    help='integral control constant')
parser.add_argument('--kd', action='store', type=float, default=0,
                    help='derivitive control constant')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
args = parser.parse_args()
tim = args.tim
calc = args.calc
cycle = args.pwm
rpsEnter = args.rps
desiredPWM = (args.rps-1.3392)/.0741
kp = args.kp
ki = args.ki
delay = args.delay * .001
sampleTime = args.sample * .001
in1 = 16
in2 = 18
en  = 22
pwm_pin = motor.motor_init(in1, in2, en, 500, desiredPWM)
motor.motor_direction(in1, in2, -1)
sleep(delay)

#Variables for collecting data
#time_start = time.time()
#cur_time = time_start
samplePosition = 0
speedPosition = 0
MAXSIZE = 2000
dataValues = [0]*MAXSIZE #array to store AD values
timeValues = [0]*MAXSIZE #array to store time
transitions = [0]*MAXSIZE #array to store where a transition occurs - 0 for no transition, 1 for transition
difference = [0]*MAXSIZE #array to store difference between AD values
rpsArray = [0]*MAXSIZE #array to most recent rps at each time
sumError = 0
error = 0
newPWM = desiredPWM
upDown = 1 #variable to see if you are looking for dark or light
maxval = 0 #maxValue used to recalculate threshold
transitionCount = 0 #Total number of transitions that have occured
transitionPosition = 0 #position in the transitions array
transitionTrack = 0 #tracker to count 1-5 transitions to see when 1 full revolution occured
firstTransitionTime = 0 #Time that the first transition in the 5 transition count occured
fifthTransitionTime = 0 #Time that the last transition in the 5 transition count occured
rps = 0 #current rps of motor
dataCount = 0 #position in array when writing data to a file
time_start = time.time()
cur_time = time_start
threshold = 20

while time_start+tim > cur_time: #Start collecting data
  pwm_pin.start(newPWM)
  if time_start + sampleTime*samplePosition< cur_time: #if enough time between samples
    dataValues[samplePosition] = mcp.read_adc(0) #get value from photoresistor
    #print(dataValues[samplePosition])
    timeValues[samplePosition] = cur_time - time_start #save current time
    if samplePosition != 0: 
      difference[samplePosition-1] =  dataValues[samplePosition] -  dataValues[samplePosition-1] #calculating difference between readings
    if difference[samplePosition-1] > threshold  and upDown == 1: #if first time past dark threshold
      transitionCount = transitionCount+1 #increment total transition count
      transitions[samplePosition] = 1 #record that a transition happened here
      upDown = -1 #look for down next
    elif difference[samplePosition-1] < threshold*-1  and upDown == -1: #if first time past light threshold
      transitionCount = transitionCount+1 #increment total transition count
      transitions[samplePosition] = 1  #record that a transition happened here
      upDown = 1 #look for up next
    else:
      transitions[samplePosition] = 0 #no new transition
      
    #calculating rps
    if time_start+ calc*speedPosition< cur_time: #if enough time has passed since last speed calculation
      transitionTrack = 0
      transitionPosition = samplePosition #position in transition array
      lookFor = 1
      #print('calc')
      while transitionTrack < 5 and transitionPosition >= 0:
        transitionTrack = transitionTrack + transitions[transitionPosition] #Adding recent transitions
        if transitionTrack == 1 and lookFor==1: 
          firstTransitionTime = timeValues[transitionPosition]
          lookFor = 2
        elif transitionTrack == 2 and lookFor==2:
          lastTransitionTime = timeValues[transitionPosition]
          lookFor = 3
        elif transitionTrack == 3 and lookFor == 3:
          lastTransitionTime = timeValues[transitionPosition]
          lookFor = 4
        elif transitionTrack == 4 and lookFor == 4:
          lastTransitionTime = timeValues[transitionPosition]
          lookFor = 5
        elif transitionTrack == 5 and lookFor == 5:
          lastTransitionTime = timeValues[transitionPosition]
          lookFor = 1
          transitionPosition = 0
        transitionPosition = transitionPosition-1 #Look at previous data point next
      if firstTransitionTime != 0 and transitionTrack>1:
        rps = (firstTransitionTime-lastTransitionTime)*(4/(transitionTrack-1))
        rps = 1/rps
        print(f'{transitionTrack}\t{firstTransitionTime}\t{lastTransitionTime}\t{rps}')
        error= rpsEnter-rps
        print(f'error {error}')
        sumError = sumError+error
        newPWM = desiredPWM+kp*error+ki*sumError
        if newPWM>100:
          newPWM = 100
        elif newPWM<0:
          newPWM = 1
        print(f'newPWM {newPWM}')
    rpsArray[samplePosition] = rps
    samplePosition = samplePosition+1
    #getting max value
    if samplePosition<100 and samplePosition>1:
      maxval = max(difference[0:100])
      threshold = .2*maxval
      if threshold < 20:
         threshold = 20
    elif samplePosition>100:
      maxval = max(difference[samplePosition-100:samplePosition])
      threshold = .2*maxval
      if threshold < 20:
         threshold = 20
  cur_time = time.time()


with open('data_kp_half.txt','w') as data:
 while dataCount < samplePosition: 
  data.write(f'{timeValues[dataCount]}\t{dataValues[dataCount]}\t{rpsArray[dataCount]}\t{transitions[dataCount]}\t{difference[dataCount]}\n')
  dataCount = dataCount + 1
