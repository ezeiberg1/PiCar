import cv2
import numpy as np

img = cv2.imread("Original.jpg")
size = (img.size)
w_size = img.shape[1]
h_size = img.shape[0]
ratio = w_size/h_size
new_width = 0
new_height = 0
if w_size>=h_size:
  new_width = 200
  new_height = int(200/ratio)
else:
  new_height = 200
  new_width = int(ratio*200)
Square200 = cv2.resize(img, (new_width, new_height), interpolation = 
cv2.INTER_AREA)
cv2.imwrite('Original_thmb.jpg', Square200)
  
