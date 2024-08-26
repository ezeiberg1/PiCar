import argparse
import time
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Function converting temperature to degrees
def convert_adc2temp (val):
   # Assuming, 3.3 supply voltage and reference voltage
   c = (val*3.3*1000.0/1023 - 500)/10
   f = 9.0/5.0*c+32
   return f
parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default=10,
                     help='time for program to run in seconds')
parser.add_argument('--delay', action='store', type=float,default=.25,
                     help='time in between messages')
parser.add_argument('--debug', action='store_true', 
                     help='specifies if debug statements are printed')
args = parser.parse_args()

if args.debug:
   print (f'arguments: {vars(args)}')
start_time = time.time()
cur_time   = start_time
mesg_time  = start_time
#Prints headers for columns
print('| {0:>4} | {1:>4} |'.format(*range(8)))
print('-' * 57) 

with open('data.txt','w') as data:
   while (start_time + args.tim > cur_time):
       time.sleep(0.001)         # some short delay to avoid busy waits
       cur_time = time.time()
       if (mesg_time + args.delay < cur_time):
          values = [0]*2
          mesg_time = cur_time
          #getting values from photo resistor
          values[0] = mcp.read_adc(0)
          values[1] = mcp.read_adc(1)
          data.write(f'{cur_time:1.0f}    {values[0]}\n')
          if values[0]>1000:
             GPIO.output(3, GPIO.HIGH)
             time.sleep(.5)
             print('dark')
             GPIO.output(3, GPIO.LOW)
             time.sleep(.5)
      # temp = mcp.read_adc(analog_pin) #Getting value from temperature sens>

     #Printing photo resistor and temperature reading
          print (values[0]) 
          print (f'Degrees F: {convert_adc2temp(values[1]):4.1f}')
GPIO.cleanup()
