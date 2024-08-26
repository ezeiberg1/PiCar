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
origDifference = [0] *(MAXSIZE-1)

i=0
for dat in data:
    values     = dat.split()          # split on white space
    times[i]    = float(values[0])     # first item in file is time
    ADvalues[i]    = float(values[1])     # second is the reading
    i=i+1

N = 1024                     # number of samples
T = 0.005                    # time between samples
t = np.linspace(0, N*T, N)  # time array


j=1
g=0
while g < len(origDifference):
  origDifference[g] = ADvalues[j]-ADvalues[j-1]
  j = j+1
  g = g+1

difference = origDifference[100:100+N]
times = times[100:100+N]

# N//4 performs int division by 4

# now calculate the fft for these signals
output = fft(difference)
freq = np.linspace(0, 1/(2*T), N//2)
plt.plot(freq, 2/N*np.abs(output[0:N//2]))
plt.grid(True)
plt.xlabel("freq - Hz")
plt.savefig("fft30.png")

plt.clf()
plt.plot(times, difference)
plt.grid()                          # show the grid
plt.ylabel('Difference in AD value')
plt.xlabel('time - sec')
plt.savefig("difference_DC_30.png")
