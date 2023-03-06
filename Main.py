import tkinter
import customtkinter
from PIL import Image, ImageTk
import cv2
import numpy as np
import speech_recognition as sr
from djitellopy import Tello
import time


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("850x510")
app.resizable(False, False)
#############
img = cv2.imread('Croc.jpg')
img = cv2.resize(img,(800,300))
###################
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
        
####################

def projectLabel():
    labelName = tkinter.StringVar(value="CSC490 Drone Project")
    label = customtkinter.CTkLabel(master=app,
                                   textvariable=labelName,
                                   width=250,
                                   height=35,
                                   font=("bold", 20),
                                   fg_color=("white", "grey23"),
                                   corner_radius=8)
    label.pack(padx=20, pady=10)

def commandButton():
    infoButton = customtkinter.CTkButton(master=app,
                                         text="Show available commands",
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
                                   placeholder_text="Enter a command: ")
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
    entrybutton.pack(padx=2, pady=5)
    testButton = customtkinter.CTkButton(master=app,
                                          text="Color Changes",
                                          command=CV2Stuff)
    testButton.pack(padx=2, pady=5)
    dronebutton = customtkinter.CTkButton(master=app,
                                          text="Click to speak to drone",
                                          command=droneEvent)
    dronebutton.pack(padx=2, pady=10)


def dronePicture():
    image1 = Image.open("images.jfif")
    img = image1.resize((200, 100), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(img)
    label1 = tkinter.Label(image=test)
    label1.image = test
    label1.pack(side=tkinter.BOTTOM)

def nothing(value):
    pass

def CV2Stuff():
    # Create a window
    cv2.namedWindow('image')


    # create trackbars for color change
    cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
    cv2.createTrackbar('SMin','image',0,255,nothing)
    cv2.createTrackbar('VMin','image',0,255,nothing)
    cv2.createTrackbar('HMax','image',0,179,nothing)
    cv2.createTrackbar('SMax','image',0,255,nothing)
    cv2.createTrackbar('VMax','image',0,255,nothing)

    # Set default value for MAX HSV trackbars.
    cv2.setTrackbarPos('HMax', 'image', 179)
    cv2.setTrackbarPos('SMax', 'image', 255)
    cv2.setTrackbarPos('VMax', 'image', 255)

    # Initialize to check if HSV min/max value changes
    hMin = sMin = vMin = hMax = sMax = vMax = 0
    phMin = psMin = pvMin = phMax = psMax = pvMax = 0

    #cam = cv2.VideoCapture(0)
    #result, frame = cam.read()

    img = cv2.imread('Croc.jpg')
    img = cv2.resize(img, (800, 300))

    cv2.resizeWindow("image",1000,800)
    output = img
    waitTime = 33

    while(1):

        # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin','image')
        sMin = cv2.getTrackbarPos('SMin','image')
        vMin = cv2.getTrackbarPos('VMin','image')

        hMax = cv2.getTrackbarPos('HMax','image')
        sMax = cv2.getTrackbarPos('SMax','image')
        vMax = cv2.getTrackbarPos('VMax','image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        output = cv2.bitwise_and(img,img, mask= mask)

        # Print if there is a change in HSV value
        if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
            print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
            phMin = hMin
            psMin = sMin
            pvMin = vMin
            phMax = hMax
            psMax = sMax
            pvMax = vMax

        # Display output image
        cv2.imshow('image',output)

        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(waitTime) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def droneEvent():
    # drone.takeoff()
    # from os import path

    # AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "take-off.wav")
    # r = sr.Recognizer()
    # with sr.AudioFile(AUDIO_FILE) as source:
    #     audio = r.record(source)
    # text = r.recognize_sphinx(audio)
    # with open("take_off.txt") as file:
    #     contents = file.read()
    #     search_word = text
    # r = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("say")
    #     r.adjust_for_ambient_noise(source)
    #     audio = r.listen(source)
    # with open("take-off.wav", "wb") as f:
    #     f.write(audio.get_wav_data())


    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print ( "Speak to the computer what commands you want your tello drone to do" )
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            text = r.recognize_sphinx(audio, keyword_entries=[("speed",0.1),("back flip", 0.1),("front flip",0.1)])
            print(text)
            # if "take off" in r.recognize_sphinx(audio, keyword_entries=[("take off", 0.1)]):
            # # Make a drone command to take off into the air
            #     drone.takeoff()
            if "land" in r.recognize_sphinx(audio, keyword_entries=[("land", 0.1)]):
            # Make a drone command to take off into the air
                drone.land()
                break
            if "battery" in r.recognize_sphinx(audio, keyword_entries=[("battery", 0.1)]):
                # Make a drone command to obtain battery
                print ( drone.get_battery() )
            if "speed" in r.recognize_sphinx(audio, keyword_entries=[("speed", 0.1)]):
                # Make a drone command to obtain speed
                print ( drone.get_speed() )
            if "back flip" in r.recognize_sphinx(audio, keyword_entries=[("back flip", 0.1)]):
                print ( drone.flip_back() )
            if "front flip" in r.recognize_sphinx(audio, keyword_entries=[("front flip", 0.1)]):
                print ( drone.flip_forward() )


drone = Tello()
#drone.connect()


dronePicture()
projectLabel()
userInput()
entryAndClear()
commandButton()

app.mainloop()