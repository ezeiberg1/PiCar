import cv2
import numpy as np

img = cv2.imread("Original.jpg")
print(f'{img.shape[1]} {img.shape[0]}')
new_width = int(input("Enter a new width:"))
ratio = img.shape[1]/img.shape[0]
new_height = int(new_width/ratio)
smaller = cv2.resize(img, (new_width, new_height), interpolation = 
cv2.INTER_AREA)
cv2.imwrite('Original_resized.jpg', smaller)
print(f'{new_width} {new_height}')

