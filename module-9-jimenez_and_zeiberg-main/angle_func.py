import cv2
import argparse
import numpy as np
import math

def getAngle(imgInput):
  #debug = debugInput
  #img = cv2.imread('test.png')
  img = cv2.imwrite('imgInput.jpg',imgInput)
  hsv = cv2.cvtColor(imgInput, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, (80, 60, 60), (130, 255, 255))
  mask_blur = cv2.blur(mask, (5,5))
  thresh = cv2.threshold(mask_blur, 200, 255, cv2.THRESH_BINARY)[1]
  cv2.imwrite('afterThresh.png', mask_blur)
  print('new image')
  M = cv2.moments(thresh)
  if M["m00"] != 0:
    cX = int(M["m10"] / M["m00"])          
    cY = int(M["m01"] / M["m00"])
    cv2.imwrite('blue_filtered.jpg', mask)
    imgCM = cv2.circle(imgInput, (cX, cY), 5, (0, 0, 255), 2)
    cv2.imwrite('blueCM.jpg', imgCM)
    angle = 0
    print(f' Cx: {cX} Cy: {cY}')
#    if debug:
 #      cv2.imshow('original img', imgInput)
  #     cv2.imshow('mask', mask)
   #    cv2.imshow('img w/ CM', imgCM)
    #   print (f'CM: ({cX}, {cY})')
     #  print(f'Angle: {angle}')
    if cX == 0 and cY == 0:
       angle = 360
    else:
       angle = math.degrees(math.atan((int(cX-imgInput.shape[1]/2))/(int(imgInput.shape[0])-cY)))
       angle = abs(angle)
       if cX > imgInput.shape[1]/2:
         angle = -angle
    return angle
  else: 
    return 360
   
