from picar import PiCar
import argparse
import time

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--mock_car', action='store_true', 
                     help='If not present, run on car, otherwise mock hardware')
args = parser.parse_args()

# test on actual hardware
car = PiCar(mock_car=args.mock_car)

tim = 5
start_time = time.time()
cur_time = start_time
delay = 1
loop_count = 0

while start_time + tim > cur_time:
   if start_time + loop_count*delay < cur_time:
      print(f'Time: {cur_time - start_time}\t AD: {car.adc.read_adc(0)}\t Distance: {car.read_distance()}')
      loop_count = loop_count + 1
   cur_time = time.time()
