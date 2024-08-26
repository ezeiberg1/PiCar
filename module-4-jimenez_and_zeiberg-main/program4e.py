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
acc    = [0]*MAXSIZE
MA_acc = [0]*MAXSIZE

i=0
for dat in data:
    values     = dat.split()          # split on white space
    time[i]    = float(values[0])     # first item in file is time
    acc[i]    = float(values[1])     # second is the acceleration
    MA_acc[i] = float(values[2])     # third is the moving average
    if DEBUG: print (f'{i}\t{time[i]}\t{dist[i]}')
    i = i + 1

# get tick marks for the x axis, in 4 regions
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

# Both on one Graph
plt.plot(time, acc, label="acc")
plt.plot(time, MA_acc, label="MovAvg")
plt.grid()                          # show the grid
plt.xlabel('time - sec')
plt.ylabel('Acceleration in g, Moving Average in g')
plt.savefig('acceleration.png')
