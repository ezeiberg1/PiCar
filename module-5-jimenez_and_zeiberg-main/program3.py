import cv2
import numpy as np
import math

img = cv2.imread("blueTape.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (80, 30, 15), (130, 90, 65))
M = cv2.moments(mask)
cX = int(M["m10"] / M["m00"])          
cY = int(M["m01"] / M["m00"])
cv2.imwrite('tape_filtered.jpg', mask)
img = cv2.circle(img, (cX, cY), 5, (0, 0, 255), 2)
cv2.imwrite('tape.jpg', img)

angle1 = math.degrees(math.atan((int(cX-img.shape[1]/2))/(int(img.shape[0])-cY)))
print(angle1)
