from scipy import signal
from scipy.fftpack import fft
import matplotlib
matplotlib.use('Agg')       # to avoid warnings if using ssh
import matplotlib.pyplot as plt
import numpy as np

fname   = input('Enter filename: ')
file    = open(fname, 'r')
data    = file.read().splitlines()  # split lines into an array 
MAXSIZE = len(data)

times    = [0]*MAXSIZE
ADvalues = [0]*MAXSIZE
rps = [0]*MAXSIZE


i=0
for dat in data:
    values     = dat.split()          # split on white space
    times[i]    = float(values[0])     # first item in file is time
    ADvalues[i]    = float(values[1])     # second is the reading
    rps[i] = float(values[2])         #third is the rps
    i=i+1



# plotting velocity
plt.clf()
plt.plot(times, rps)
plt.grid()                          # show the grid
plt.ylabel('Velocity')
plt.xlabel('time - sec')
plt.savefig("plot_kp_half.png")
