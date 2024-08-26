
from mod4_funcs import movingAvg
import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)
DEBUG   = False                     # For printing debug statements

time    = [0]*MAXSIZE
accUp = [0]*MAXSIZE
accTurn = [0]*MAXSIZE
vel = [0]*MAXSIZE
velAvg = [0]*MAXSIZE
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
    vel[i] = float(values[6])
    velAvg[i] = movingAvg(vel, i)        # fifth is average velocity
    if DEBUG: print (f'{i}\t{time[i]}\t{dist[i]}')
    i = i + 1

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[67], time[79], 5) 
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
plt.subplot(111)
plt.grid()                          # show the grid
plt.plot(time[67:79], velAvg[67:79])
plt.xlabel('time-sec')
plt.ylabel('vel in CM/s')
plt.savefig("velocity.png")
