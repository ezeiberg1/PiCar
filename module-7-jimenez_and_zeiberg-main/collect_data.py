import argparse
import time			#import SMBus module of I2C
from time import sleep 
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
import mod7_func as motor

GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--tim', action='store', type=int, default = 5,
                    help = 'Run Time in seconds')
parser.add_argument('--delay', action='store', type=float, default= 10,
                    help='Time in between readings in milliseconds')
parser.add_argument('--cycle', action='store', type=int, default=50,
                    help='Duty Cycle in percent')
parser.add_argument('--debug', action='store_true',
                    help='specifies if debug statements are printed')
args = parser.parse_args()
tim = args.tim
cycle = args.cycle
delay = args.delay * .001
time_start = time.time()
cur_time = time_start
dataCount = 0
loop_count = 0
dataValues = [0]* int(tim/delay)
timeValues = [0] * int(tim/delay)
values = [0] * int(tim/delay)
in1 = 16
in2 = 18
en  = 22
pwm_pin   = motor.motor_init(in1, in2, en, 500, cycle)

motor.motor_direction(in1, in2, 1)
sleep(1)
while time_start+tim > cur_time:
  if time_start + delay*loop_count< cur_time:
       #getting values from photo resistor
    dataValues[loop_count] = mcp.read_adc(0)
    timeValues[loop_count] = cur_time - time_start
    loop_count = loop_count + 1
  cur_time = time.time()
  
with open('data_90.txt','w') as data:
  while dataCount < len(dataValues): 
    data.write(f'{timeValues[dataCount]}\t{dataValues[dataCount]}\n')
    dataCount = dataCount + 1
    
GPIO.cleanup()
