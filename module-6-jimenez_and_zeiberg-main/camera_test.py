from picamera import PiCamera
import picamera.array
import time
import cv2

t1 = time.time()
camera = PiCamera()
camera.framerate = 30
stream = picamera.array.PiRGBArray(camera)  # Create the stream

t2 = time.time()
camera.capture('testing1.png')         # Take & save large image

t3 = time.time()
camera.resolution = (320, 208)
camera.capture('testing2.png')         # Take & save smaller image

t4 = time.time()
camera.capture(stream, format='bgr')   # Save directly to memory
image = stream.array
stream.truncate(0)                     # needed to take another pic

t5 = time.time()
cv2.imwrite('testing3.png', image)     # Save the image from memory

t6 = time.time()                       # stream image directly from port
camera.capture(stream, format='bgr', use_video_port=True)   
image = stream.array
stream.truncate(0)                     # needed to take another pic

t7 = time.time()
cv2.imwrite('testing4.png', image)     # Save second image from memory
t8 = time.time()

print (f'Framerate: {camera.framerate}')
print (f'time to setup object PiCamera: {t2-t1:1.3f}')
print (f'time to take and save first picture: {t3-t2:1.3f}')
print (f'time to take and save smaller picture: {t4-t3:1.3f}')
print (f'time to take streamed image: {t5-t4:1.3f}')
print (f'time to save streamed image: {t6-t5:1.3f}')
print (f'time to take with use_video_port directly & stream: {t7-t6:1.3f}')
print (f'time to save streamed image: {t8-t7:1.3f}')
