#!/usr/bin/env python

#####################################################################
#   code developed by: austinmeier
#   developed on: 
#   contact:austinmeier on github
#####################################################################
#                       Imports here
#####################################################################
import time
import os
from time import sleep
import RPi.GPIO as GPIO

#####################################################################
#                           Variables
#####################################################################






#####################################################################
#                       Define functions
#####################################################################

#####################################################################
GPIO.setmode(GPIO.BCM)

def main():
    color= (light_chose())
    behavior = (onoff(color))
    if color == "red":
        red(behavior)
    elif color == "green":
        green(behavior)
    elif color == "both":
        red(behavior)
        green(behavior)





def light_chose():
    light=str(raw_input("Which light would you like to modify? (red/green)"))
    #if light != "red" or light != "green":
    #    print light
    #    print('Sorry, that color choice is not recognized.  Please try again.')
    #    light_chose()
    #else: return light
    return light


def onoff(color):
    choice=raw_input("Would you like the %s light on or off?"%(color))
    #if choice != "on" or choice != "off":
    #    print("Sorry, that behavior choice is not recognized.  Please try again.")
    #    onoff(color)
    #else: return choice
    return choice





def red(x):
    if x == "on":
        print("Red light is ON.")
        GPIO.output(27,GPIO.HIGH)
    elif x == "off":
        print("Red light is OFF.")
        GPIO.output(27,GPIO.LOW)
    elif x == "flash":
        print("Red light is flashing")
        GPIO.output(27,GPIO.HIGH)   #on
        time.sleep(.5)              #remain on
        GPIO.output(27,GPIO.LOW)    #off
        time.sleep(1)
        GPIO.output(27,GPIO.HIGH)   #on
        time.sleep(.5)              #remain on
        GPIO.output(27,GPIO.LOW)    #off
        time.sleep(1)
        GPIO.output(27,GPIO.HIGH)   #on
        time.sleep(.5)              #remain on
        GPIO.output(27,GPIO.LOW)    #off

        

def green(x):
    if x == "on":
        print("Green light is ON.")
        GPIO.output(17,GPIO.HIGH)
    elif x == "off":
        print("Green light is OFF.")
        GPIO.output(17,GPIO.LOW)
    elif x == "flash":
        print("Green light is flashing")
        GPIO.output(17,GPIO.HIGH)   #on
        time.sleep(.5)              #remain on
        GPIO.output(17,GPIO.LOW)    #off
        time.sleep(1)
        GPIO.output(17,GPIO.HIGH)   #on
        time.sleep(.5)              #remain on
        GPIO.output(17,GPIO.LOW)    #off
        time.sleep(1)
        GPIO.output(17,GPIO.HIGH)   #on
        time.sleep(.5)              #remain on
        GPIO.output(17,GPIO.LOW)    #off





#####################################################################
#                     Put code below this
#####################################################################
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(True)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)



while True:
    main()
