import matplotlib
matplotlib.use('Pdf')               # We are just printing
import matplotlib.pyplot as plt
import numpy as np

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)
DEBUG   = False   


time    = [0]*MAXSIZE
ADvalues = [0]*MAXSIZE
difference = [0] *MAXSIZE

i=0
for dat in data:
    values     = dat.split()          # split on white space
    time[i]    = float(values[0])     # first item in file is time
    ADvalues[i]    = float(values[1])     # second is the reading
    if DEBUG: print (f'{i}\t{time[i]}\t{ADvalues[i]}')
    i = i + 1
    
xmarks = np.linspace(time[0], time[MAXSIZE - 1], 5) 
plt.xticks(xmarks)

j=1
difference[0] = 0
while j < MAXSIZE:
  difference[j] = ADvalues[j]-ADvalues[j-1]
  j = j+1

plt.clf()                           # start new plot
plt.figure()
plt.subplot(121)
plt.grid()                          # show the grid
plt.plot(time, ADvalues)
plt.ylabel('AD Value')
plt.subplot(122)
plt.plot(time, difference)
plt.grid()                          # show the grid
plt.ylabel('Difference in AD value')
plt.xlabel('time - sec')
plt.savefig("photo_DC_90.png")
