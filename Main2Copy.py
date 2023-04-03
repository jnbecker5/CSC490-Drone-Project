import atexit

from djitellopy import Tello
import threading
import time
from time import sleep
import cv2
import numpy as np
import time
#import ColorSlider
from threading import Thread



try:
    drone = Tello()
    drone.connect()
    print(drone.get_battery())
    print("ok so ignore all of the errors")
    drone.streamon()
    print("we don't know how to make them go away")
    frame_read = drone.get_frame_read()
    print("but the program still functions")
    trackBool = False
    dist = 50
    cX = 0
    cY = 0
    angle = 10


    def nothing(x):
        pass

    cv2.namedWindow('image')
    cv2.namedWindow('Video')

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

    cv2.setTrackbarPos('HMin', 'image', 37)
    cv2.setTrackbarPos('SMin', 'image', 49)
    cv2.setTrackbarPos('HMax', 'image', 94)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 149)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0




    def command():
        loop = True
        while loop:
            time.sleep(1)
            msg = input("Enter a command: ")
            if msg == "t":
                try:
                    print("Drone battery is at: " + str(drone.get_battery()))
                    drone.takeoff()
                    sleep(2)
                except: #Exception("Command '{}' was unsuccessful for {} tries. Latest response:\t'{}'") as e:
                    print("Take off failed")
            elif msg == "l":
                drone.land()
                trackBool = False
            elif msg == "right":
                drone.rotate_clockwise(90)
            elif msg == "left":
                drone.rotate_counter_clockwise(90)
            elif msg == "s":
                trackThread = threading.Thread(target=track)
                trackThread.start()
            elif msg == "b":
                print("Drone battery is at: " + str(drone.get_battery()))
            elif msg == "x":
                loop = False
    def track():
        endTime = time.time() + 15
        trackBool = True
        print("Tracking started")
        while time.time()<endTime and trackBool:
            mult = 50
            centerThresh = 10
            heightDiff = int(abs((cY - (height / 2)) / (height / 2)) * mult)
            angle = int(abs((cX - (width / 2)) / (width / 2)) * mult)
            valX = angle * 3
            valY = heightDiff * 2
            if cX > ((width / 2)+centerThresh):
                rot = valX
                #drone.rotate_clockwise(angle)
            elif cX < ((width / 2)-centerThresh):
                rot = -valX
                #drone.rotate_counter_clockwise(angle)
            else:
                rot = 0
            if cY >((height/2) + centerThresh):
                vert = -valY
                #drone.move_down(30)
            elif cY < ((height / 2) - centerThresh):
                vert = valY
                #drone.move_up(30)
            else:
                vert = 0
            drone.send_rc_control(0,0,vert,rot)
            sleep(.1)
        print("Tracking ended")
        vert = 0
        rot = 0
        drone.send_rc_control(0, 0, vert, rot)

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
        #cv2.circle(thresh, (cX, cY), 5, (255, 255, 255), -1)
        #cv2.putText(thresh, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 90, 60), 2)

        cv2.circle(output, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(output, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 90, 60), 2)

        # display the image
        cv2.imshow("Video", output)
        cv2.waitKey(1)
finally:
    print("drone disconnecting")
    drone.end()
    sleep(3)
    print("drone disconnected")
