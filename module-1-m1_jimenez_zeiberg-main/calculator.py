import argparse
import time

def sumFunc(a,b):
  sum = a+b;
  return sum;

def prodFunc(a,b):
  prod = a * b;
  return prod;

def powFunc(a,b):
  pow = a**b;
  return pow;

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--debug', action='store_true',
		    help='specifies if debug statements are printed.')
parser.add_argument('--a', action='store', type=float, default=2,
		    help='first number')
parser.add_argument('--b', action='store', type=float, default=2,
                    help='second number')
parser.add_argument('--op', action='store', type=float, default=2,
                    help='Operation: 1 = Sum, 2 = Product, 3 = Power')
args = parser.parse_args()

if args.debug:
  print (f'arguments: {vars(args)}')
a = args.a
b = args.b
oper = args.op
answer = 0

if (oper == 1):
  answer = sumFunc(a,b)
  print(f'Sum: {answer:0.3f}') 

if (oper == 2):
  answer = prodFunc(a,b)
  print(f'Product: {answer:0.3f}')

if (oper == 3):
  answer = powFunc(a,b)
  print(f'Raised to Power: {answer:0.3f}')

while (args.debug):
  curr_time = time.time()
  time.sleep(.001)
  print(f'curr_time: {curr_time:0.3f}')
