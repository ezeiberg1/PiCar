import argparse
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Data for this program.')
parser.add_argument('--r', action='store', type=float, default = 5,
                    help = 'row pixel')
parser.add_argument('--c', action='store', type=float, default=5,
                    help='column pixel')
args = parser.parse_args()
row = int(args.r)
column = int(args.c)

img = cv2.imread("blueTape.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_value = hsv[row, column]
print(hsv_value)
img = cv2.circle(img, (column, row), 5, (0, 255, 0), 2)
cv2.imwrite('tapeCircle.png', img)
