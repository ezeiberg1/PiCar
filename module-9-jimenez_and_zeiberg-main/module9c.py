import argparse
import time			#import SMBus module of I2C
from time import sleep 
from picar import PiCar
from scipy import signal
from scipy.fftpack import fft
import matplotlib
matplotlib.use('Agg')       # to avoid warnings if using ssh
import matplotlib.pyplot as plt
import numpy as np

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
parser.add_argument('--mock_car', action='store_true', 
                     help='If not present, run on car, otherwise mock hardware')
args = parser.parse_args()
car = PiCar(mock_car=args.mock_car)
tim = args.tim
calc = args.calc
cycle = args.pwm
rpsEnter = args.rps
desiredPWM = (args.rps-1.3392)/.0741
kp = args.kp
ki = args.ki
delay = args.delay * .001
sampleTime = args.sample * .001
car.set_motor(desiredPWM)
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
  car.set_motor(newPWM)
  if time_start + sampleTime*samplePosition< cur_time: #if enough time between samples
    dataValues[samplePosition] = car.adc.read_adc(0) #get value from photoresistor
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


with open('data_9c_usingCar.txt','w') as data:
 while dataCount < samplePosition: 
  data.write(f'{timeValues[dataCount]}\t{dataValues[dataCount]}\t{rpsArray[dataCount]}\t{transitions[dataCount]}\t{difference[dataCount]}\n')
  dataCount = dataCount + 1
  
  
file    = open('data_9c_usingCar.txt', 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)

timesPlot    = [0]*MAXSIZE
ADvaluesPlot = [0]*MAXSIZE
rpsPlot = [0]*MAXSIZE


i=0
for dat in data:
    valuesPlot     = dat.split()          # split on white space
    timesPlot[i]    = float(valuesPlot[0])     # first item in file is time
    ADvaluesPlot[i]    = float(valuesPlot[1])     # second is the reading
    rpsPlot[i] = float(valuesPlot[2])         #third is the rps
    i=i+1



# plotting velocity
plt.clf()
plt.plot(timesPlot, rpsPlot)
plt.grid()                          # show the grid
plt.ylabel('Velocity')
plt.xlabel('time - sec')
plt.savefig("plot_9c.png")

N = 1024                     # number of samples
T = 0.005                    # time between samples
t = np.linspace(0, N*T, N)  # time array

origDifference = [0] *(MAXSIZE-1)

j=1
g=0
while g < len(origDifference):
  origDifference[g] = ADvaluesPlot[j]-ADvaluesPlot[j-1]
  j = j+1
  g = g+1

difference = origDifference[100:100+N]
timesPlot = timesPlot[100:100+N]

# N//4 performs int division by 4

# now calculate the fft for these signals
plt.clf()
output = fft(difference)
freq = np.linspace(0, 1/(2*T), N//2)
plt.plot(freq, 2/N*np.abs(output[0:N//2]))
plt.grid(True)
plt.xlabel("freq - Hz")
plt.savefig("fft_9c_usingCar.png")
