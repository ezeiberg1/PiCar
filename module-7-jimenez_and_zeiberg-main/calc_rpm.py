from mod7_func import movingAvg
import time
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import numpy as np 
fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)
DEBUG   = False   

#Creating Arrays and variables
times    = [0]*MAXSIZE
ADvalues = [0]*MAXSIZE
origDifference = [0] *(MAXSIZE-1)
lightDarkArr = [0] *(MAXSIZE-1)
arrAvg = [0] * (MAXSIZE-1)
position = 0
cur_time = time.time()
reading = 0
arrAll = [0]*100

#Adding data from file to arrays
i=0
for dat in data:
    values     = dat.split()          # split on white space
    times[i]    = float(values[0])     # first item in file is time
    ADvalues[i]    = float(values[1])     # second is the reading
    if DEBUG: print (f'{i}\t{time[i]}\t{ADvalues[i]}')
    i = i + 1
    
#Calculating the differenece between each sample
j=1
g=0
while g < len(origDifference):
  origDifference[g] = ADvalues[j]-ADvalues[j-1]
  j = j+1
  g = g+1

#Calculating the moving avarage of the differences
loop_count = 0
k = 0
difference = origDifference[20:]
newTimes = times[1:len(difference)]
while k < len(difference):
  arrAvg[position] = movingAvg(difference, position, 3, 0)
  position = position + 1
  loop_count = loop_count+1
  cur_time = time.time() 
  k = k+1
#Finding max
m = 0
max = 0
while m < len(arrAvg):
  if arrAvg[m] > max:
    max = arrAvg[m]
  m = m + 1

#Finding min
n = 0
min = max
while n < len(arrAvg):
  if arrAvg[n] < min:
    min = arrAvg[n]
  n = n + 1

average = (max+min)/2
threshold = .2*average
transition = 0
upDown = 1
h = 20
p=0

while h < len(difference):
    if arrAvg[h] > average+threshold  and upDown == 1: #if first time past dark threshold
        transition = transition + 1
        upDown = -1
        lightDarkArr[h] = 1
    elif arrAvg[h] < average-threshold  and upDown == -1: #if first time past light threshold
        transition = transition + 1
        upDown = 1
        lightDarkArr[h] = -1
    else:
        lightDarkArr[h] = 0
    h = h+1
dataCount = 0 
with open('lightDark.txt','w') as data:
 while dataCount < len(lightDarkArr): 
  data.write(f'{times[dataCount]}\t{lightDarkArr[dataCount]}\n')
  dataCount = dataCount + 1

#calculating rpm
rpm = (transition/4)/(times[len(times)-1]-times[20])*60
print(rpm)

plt.clf()                           # start new plot
plt.figure()
plt.grid()                          # show the grid
plt.plot(times[20:], lightDarkArr[0:len(lightDarkArr)-19])
plt.ylabel('Detection of Color Change')
plt.xlabel('time - sec')
plt.savefig('cycle90.png')
print(transition)
q = 0
while q<len(lightDarkArr)-19:
   print(lightDarkArr[q])
   q = q+1
