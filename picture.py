import picamera
import time
import StringIO

pic = raw_input("please enter name of photo: ")



print("taking picture in 5")
time.sleep(1)
print("taking picture in 4")
time.sleep(1)
print("taking picture in 3")
time.sleep(1)
print("taking picture in 2")
time.sleep(1)
print("taking picture in 1")
time.sleep(1)
print("taking picture")
with picamera.PiCamera() as camera:
    camera.resolution = (1280,720)
    camera.capture("/home/pi/ISAAC/pictures/"+ pic +".jpg")

print("picture taken")
