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

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(True)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)


#####################################################################
#                       Define functions
#####################################################################

#####################################################################

def main():
    color= (light_chose())
    behavior = (onoff(color))
    if color == "red":
        red(behavior)
    elif color == "green":
        green(behavior)
    elif color == "yellow":
        yellow(behavior)
 
    elif color == "all":
        red(behavior)
        green(behavior)
        yellow(behavior)




def light_chose():
    color_options = ["red","green","yellow","all"]
    light=str(raw_input("Which light would you like to modify? (red/green/yellow/all)"))
    if light not in color_options:
        print('Sorry, that color choice is not recognized.  Please try again.')
        light_chose()
    else: return light


def onoff(color):
    behavior_options = ["on","off","flash"]
    
    choice = [str(x) for x in raw_input("How would you like the %s light to behave? (on, off, flash x)"%(color)).split()]
    print(choice)
    if choice[0] not in behavior_options:
        print("Sorry, that behavior choice is not recognized.  Please try again.")
        onoff(color)
    else: return choice





def red(x):
    print x
    if x[0] == "on":
        print("Red light is ON.")
        GPIO.output(27,GPIO.HIGH)
    elif x[0] == "off":
        print("Red light is OFF.")
        GPIO.output(27,GPIO.LOW)
    elif x[0] == "flash":
        flashnumber = 3
        if len(x)>1:
            print ("Red light will flash %s times."%x[1])
            flashnumber = int(x[1])
        else:
            print("Red light will flash 3 times.")
        for i in range(flashnumber):
            time.sleep(.5)
            GPIO.output(27,GPIO.HIGH)   #on
            time.sleep(.5)              #remain on
            GPIO.output(27,GPIO.LOW)    #off
        

def green(x):
    print x
    if x[0] == "on":
        print("Green light is ON.")
        GPIO.output(17,GPIO.HIGH)
    elif x[0] == "off":
        print("Green light is OFF.")
        GPIO.output(17,GPIO.LOW)
    elif x[0] == "flash":
        flashnumber = 3
        if len(x)>1:
            print ("Green light will flash %s times."%x[1])
            flashnumber = int(x[1])
        else:
            print("Green light will flash 3 times.")
        for i in range(flashnumber):
            time.sleep(.5)
            GPIO.output(17,GPIO.HIGH)   #on
            time.sleep(.5)              #remain on
            GPIO.output(17,GPIO.LOW)    #off
        

def yellow(x):
    print x
    if x[0] == "on":
        print("Yellow light is ON.")
        GPIO.output(18,GPIO.HIGH)
    elif x[0] == "off":
        print("Yellow light is OFF.")
        GPIO.output(18,GPIO.LOW)
    elif x[0] == "flash":
        flashnumber = 3
        if len(x)>1:
            print ("Yellow light will flash %s times."%x[1])
            flashnumber = int(x[1])
        else:
            print("Yellow light will flash 3 times.")
        for i in range(flashnumber):
            time.sleep(.5)
            GPIO.output(18,GPIO.HIGH)   #on
            time.sleep(.5)              #remain on
            GPIO.output(18,GPIO.LOW)    #off
        


#####################################################################
#                     Put code below this
#####################################################################


while True:
    main()
