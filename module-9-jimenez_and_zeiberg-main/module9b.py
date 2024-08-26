from picar import PiCar
import argparse
import time

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--mock_car', action='store_true', 
                     help='If not present, run on car, otherwise mock hardware')
parser.add_argument('--tim', action='store', type=float, default = 10,
                     help = 'Run Time in seconds')
args = parser.parse_args()

# test on actual hardware
car = PiCar(mock_car=args.mock_car)

tim = args.tim
start_time = time.time()
cur_time = start_time
delay = .005
loop_count = 0
distance = 0
car.set_motor(0)

while start_time + tim > cur_time:
   if start_time + loop_count*delay < cur_time:
      distance  = car.read_distance()
      print(distance)
      if distance < 10:
         print('<10')
         car.set_motor(0)
      elif distance < 50:
         newSpeed = 10 * (distance / 5)
         car.set_motor(newSpeed)
         print('<50')
      else:
         car.set_motor(0)
         print('>50')
      loop_count = loop_count + 1
   cur_time = time.time()
