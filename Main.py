import math
import tkinter
import customtkinter
from PIL import Image, ImageTk
import cv2
import numpy as np
import speech_recognition as sr
from djitellopy import Tello
import time
from time import sleep
import threading
from threading import Thread

#Create main UI window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("850x510")
app.resizable(False, False)
img = cv2.imread('Croc.jpg')
img = cv2.resize(img,(800,300))

#Create secondary window for when user clicks "Show available Commands"
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("270x250")

        # self.label = customtkinter.CTkLabel(self, text="HMin")
        # self.label.pack(padx=2, pady=5)
        # self.slider1 = customtkinter.CTkSlider(self, from_=0, to=179, command=ToplevelWindow.slider_event)
        # self.slider1.pack(padx=5,pady=5)

        # self.label = customtkinter.CTkLabel(self, text="SMin")
        # self.label.pack(padx=2, pady=5)
        # self.slider2 = customtkinter.CTkSlider(self, from_=0, to=255, command=ToplevelWindow.slider_event)
        # self.slider2.pack(padx=5,pady=5)
        self.dialog = customtkinter.CTkTextbox(self,
                                        width=200,
                                        corner_radius=20)
        self.dialog.pack(padx=20, pady=10)
        self.dialog.insert("0.0", "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n"
                            "Placeholder\n")
        self.dialog.configure(state="disabled")

#Main window label
def projectLabel():
    labelName = tkinter.StringVar(value="Drone Project")
    label = customtkinter.CTkLabel(master=app,
                                   textvariable=labelName,
                                   width=250,
                                   height=35,
                                   font=("bold", 20),
                                   fg_color=("white", "grey23"),
                                   corner_radius=8)
    label.pack(padx=20, pady=10)

#Button which initializes TopLevelWindow class
def commandButton():
    infoButton = customtkinter.CTkButton(master=app,
                                         text="Show Available Commands",
                                         command=ToplevelWindow)
    infoButton.pack(side=tkinter.BOTTOM, pady=10)

# def commandButtonEvent():
#     dialog = customtkinter.CTkTextbox(master=app,
#                                       width=200,
#                                       corner_radius=20)
#     dialog.pack(padx=20, pady=10)
#     dialog.insert("0.0", "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n"
#                          "Placeholder\n")
#     dialog.configure(state="disabled")


def userInput():
    global entry
    entry = customtkinter.CTkEntry(master=app,
                                   placeholder_text="Enter a Command: ")
    entry.pack(padx=20, pady=10)

def enterFunction():
    global testing
    testing = entry.get()
    entry.delete(0, tkinter.END)
    print(testing)


def clearFunction():
    entry.delete(0, tkinter.END)

def entryAndClear():
    entrybutton = customtkinter.CTkButton(master=app,
                                          text="Enter",
                                          command=enterFunction)
    entrybutton.pack(padx=2, pady=40)
    testButton = customtkinter.CTkButton(master=app,
                                          text="Object Tracking",
                                          command=CV2Stuff)
    testButton.pack(padx=2, pady=5)
    dronebutton = customtkinter.CTkButton(master=app,
                                          text="Voice Control",
                                          command=droneEventStart)
    dronebutton.pack(padx=2, pady=10)

def droneEventStart():
    voiceThread = threading.Thread(target=droneEvent)
    voiceThread.start()



def dronePicture():
    image1 = Image.open("images.jfif")
    img = image1.resize((200, 100), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label1.pack(side=tkinter.BOTTOM)

def nothing(value):
    pass

def CV2Thread():
    CVThread = threading.Thread(target=CV2Stuff)
    CVThread.start()

def CV2Stuff():
    try:
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
        def back():
            cv2.destroyWindow('Video')
            cv2.destroyWindow('image')
        #



        # create trackbars for color change
        cv2.createTrackbar('HMin', 'image', 0, 179, nothing)  # Hue is from 0-179 for Opencv
        cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
        cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
        cv2.createTrackbar('HMax', 'image', 0, 179, nothing)
        cv2.createTrackbar('SMax', 'image', 0, 255, nothing)
        cv2.createTrackbar('VMax', 'image', 0, 255, nothing)
        cv2.createTrackbar('Dont Touch This', 'image', 0, 1,back)

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
        #drone.end()
        drone.streamoff()
        sleep(3)
        print("drone disconnected")

def droneEvent():
    drone.takeoff()
    drone.set_speed(60)
    r = sr.Recognizer()
    r.energy_threshold = 2000
    # AUDIO_FILE = "take-off.wav"

    # with sr.AudioFile(AUDIO_FILE) as source:
    #     audio = r.record(source)
    # print(x)


    breakCase = True
    while (breakCase == True):

        try:
            with sr.Microphone() as source:

                drone.get_battery()
                print ( "Speak to the computer what commands you want your tello drone to do" )
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                #Create an instance of speech recognition
                x = r.recognize_google(audio)

######################################

                #Commands to make it stop.
                if "stop" in x:
                    drone.land()
                    print("Stopping!")
                    breakCase = False
                if "help land the drone" in x:
                    drone.land()
                    print("Stopping!")
                    breakCase = False
                if "its flying away" in x:
                    drone.land()
                    print("Stopping!")
                    breakCase = False
                if "break" in x:
                    drone.land()
                    print("Stopping!")
                    breakCase = False
                if "land" in x:
                    # Make a drone command to land
                    drone.land()
                    breakCase = False

######################################

                else:

                    if "take off" in x:
                    #  Make a drone command to take off into the air
                        drone.takeoff()

                    if "play dead" in x:
                    # Make a drone command to land
                        drone.land()
                    
                    if "rotate left" in x:
                        drone.rotate_clockwise(90)
                    
                    if "rotate right" in x:
                        drone.rotate_counter_clockwise(90)

                    if "speed" in x:
                    # Make a drone command to obtain speed
                        print ( drone.get_speed() )

                    if "backflip" in x:
                    # Make drone flip backward
                        drone.flip_back()

                    if "front flip" in x:
                    # Make drone flip forward
                        drone.flip_forward()

                    if "move left" in x:
                    # Make the drone move left
                        drone.move_left(50)

                    if "move right" in x:
                    # Make the drone move right
                        drone.move_right(50)

                    if "move forward" in x:
                    # Make the drone move forward
                        drone.move_forward(50)

                    if "move back" in x:
                    # Make the drone move backward
                        drone.move_back(50)

                    if "move up" in x:
                    # Make the drone move up
                        drone.move_up(50)

                    if "go for a walk" in x:
                    # Make the drone move around "randomly"
                        drone.move_forward(100)
                        drone.rotate_counter_clockwise(90)
                        drone.move_forward(100)
                        drone.rotate_counter_clockwise(90)
                        drone.move_forward(100)
                        drone.rotate_counter_clockwise(90)
                        drone.move_forward(100)
                        drone.rotate_counter_clockwise(90)

                    if "shake and bake" in x:
                    # Make the drone "go crazy"
                        drone.flip_back()
                        drone.flip_left()
                        drone.flip_left()

        except:
            print("I didn't understand, please try again!")
            droneEvent()

drone = Tello()
drone.connect()

dronePicture()
projectLabel()
userInput()
entryAndClear()
commandButton()

app.mainloop()
