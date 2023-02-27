from djitellopy import Tello
import threading
import time
from time import sleep
import cv2
import numpy as np
#import ColorSlider
from threading import Thread


drone = Tello()
drone.connect()
print(drone.get_battery())
print("ok so ignore all of the errors")
drone.streamon()
print("we don't know how to make them go away")
frame_read = drone.get_frame_read()
print("but the program still functions")
dist = 50
cX = 0
cY = 0
angle = 10

def nothing(x):
    pass

cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)  # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 0, 255, nothing)

# Set default value for MAX HSV trackbars.
cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0




def command():
    loop = True
    while loop:
        time.sleep(1)
        msg = input("Enter a command: ")
        if msg == "t":
            drone.takeoff()
        elif msg == "l":
            drone.land()
            trackThread.terminate()
        elif msg == "right":
            drone.rotate_clockwise(90)
        elif msg == "left":
            drone.rotate_counter_clockwise(90)
        elif msg == "s":
            trackThread = threading.Thread(target=track)
            trackThread.start()
        elif msg == "c":
            drone.send_command_with_return("takeoff")
        elif msg == "x":
            loop = False
def track():
    while True:
        angle = int(abs((cX - (width / 2)) / (width / 2)) * 60)
        if cX > ((width / 2)+50):
            drone.rotate_clockwise(angle)
        elif cX < ((width / 2)-50):
            drone.rotate_counter_clockwise(angle)
        if cY >((height/2) + 50):
            drone.move_down(30)
        elif cY < ((height / 2) - 50):
            drone.move_up(30)
        sleep(.1)

commandThread = threading.Thread(target=command)
commandThread.start()
drone.streamon()

while True:
    img = drone.get_frame_read().frame
    width = 720
    height = 480
    img = cv2.resize(img, (width, height))

    imgSlide = img

    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')

    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')
    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    hsv = cv2.cvtColor(imgSlide, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(imgSlide, imgSlide, mask=mask)

    # Print if there is a change in HSV value
    if ((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax)):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (
        hMin, sMin, vMin, hMax, sMax, vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    #ORANGE_MIN = np.array([0, 50, 50], np.uint8)
    #ORANGE_MAX = np.array([15, 255, 255], np.uint8)

    hsv_img = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)

    thresh = cv2.inRange(hsv_img, lower, upper)
    # convert image to grayscale image
    #gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # convert the grayscale image to binary image
    #ret, thresh = cv2.threshold(gray_image, 127, 255, 0)

    # calculate moments of binary image
    M = cv2.moments(thresh)

    # calculate x,y coordinate of center
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    #print("X: "+str(cX) + "and Y: " + str(cY))
    # put text and highlight the center
    cv2.circle(thresh, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(thresh, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 90, 60), 2)

    # display the image
    cv2.imshow("image", thresh)
    cv2.waitKey(1)