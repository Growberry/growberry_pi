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
    print("result of light_chose function:  %s"%(color))
    behavior = (onoff(color))
    print("result of behavior function:  %s"%(behavior))
    
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
    else: print("sum-ting-wong")



def light_chose():
    color_options = ["red","green","yellow","all"]
    light=str(raw_input("Which light would you like to modify? (red/green/yellow/all)"))
    if light not in color_options:
        print('Sorry, that color choice is not recognized.  Please try again.')
        return light_chose()
    else: return light


def onoff(color):
    behavior_options = ["on","off","flash"]
    
    choice = [str(x) for x in raw_input("How would you like the %s light to behave? (on, off, flash x)"%(color)).split()]
    print(choice)
    if choice[0] not in behavior_options:
        print("Sorry, that behavior choice is not recognized.  Please try again.")
        return onoff(color)
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



try:  
    # here you put your main loop or block of code  
    while True:
        main()
    while counter < 9000000:  
        # count up to 9000000 - takes ~20s  
        counter += 1  
    print "Target reached: %d" % counter  
  
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "\n", counter # print value of counter  
  
except:  
    # this catches ALL other exceptions including errors.  
    # You won't get any error messages for debugging  
    # so only use it once your code is working  
    print "Other error or exception occurred!"  
  
finally:  
    GPIO.cleanup() # this ensures a clean exit 




