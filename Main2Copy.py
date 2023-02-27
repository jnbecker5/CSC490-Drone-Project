from djitellopy import Tello
import threading
import time
from time import sleep
import cv2
import numpy as np
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

    ORANGE_MIN = np.array([0, 50, 50], np.uint8)
    ORANGE_MAX = np.array([15, 255, 255], np.uint8)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    thresh = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
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
    cv2.imshow("Image", thresh)
    cv2.waitKey(1)

while False:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (720, 480))

    hav = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    sensitivity = 50

    lower_white = np.array([0,0,255 - sensitivity])
    upper_white = np.array([180,sensitivity,255])

    mask = cv2.inRange(hav,lower_white,upper_white)
    res = cv2.bitwise_and(img,img,mask=mask)

    M = cv2.moments(res)

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.putText(img, "centroid",(cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)

    cv2.imshow("Image", img)
    cv2.imshow("mask",mask)
    cv2.imshow("res",res)

    cv2.waitKey(1)
