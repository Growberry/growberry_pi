#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier                                  #
#   developed on: 03/25/2016                                        #
#   contact:austinmeier on github                                   #
#####################################################################
"""

###########################  Imports here  ##########################
from threading import Thread
import time
import os
from time import sleep
import RPi.GPIO as GPIO

#####################################################################
#                           GPIO pin set up
#####################################################################
#select one of these two modes:
GPIO.setmode(GPIO.BCM)      #for using the names of the pins
#or
#GPIO.setmode(GPIO.BOARD)   #for true pin number IDs (pin1 = 1)

GPIO.cleanup()             #shouldn't need to use this, but just in case

GPIO.setwarnings(False)      #set to false if the warnings bother you, helps troubleshooting

############################ Activating pins ########################
#GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(17,GPIO.OUT, initial = 0)
GPIO.setup(27,GPIO.OUT, initial = 0)
GPIO.setup(18,GPIO.OUT, initial = 1)


########################### if pin is GPIO.OUT  ######################

#turning the pins on or off

#GPIO.output(18,GPIO.HIGH)   #on
#GPIO.output(18,GPIO.LOW)    #off


##########################  if pin is GPIO.IN  ########################




#####################################################################
#                           Classes
#####################################################################
from class_relay import LED 

####################################################################
greenLED= LED(17,"greenLED","green", 20)
redLED= LED(27,"redLED","red", 20)
yellowLED= LED(18,"yellowLED","yellow", 20)

#####################################################################
#                     Put code below this
#####################################################################

def main():
    """
    loop asking for an activity code via raw input. Exits by typing 'exit'
    """
    print('\n\n\n\n\n[--system--] enter code for LED behavior: LEDname on/off/strobe\n')
    print('\nconnecting....')
    bootseq(1,4)
    time.sleep(.2)
    print('....')
    time.sleep(.2)
    print('....')
    time.sleep(1)
    print('....')
    time.sleep(.5)
    print('connection established\n')
    print('----------------------------')
    print('  WELCOME TO THE LIGHTSHOW  ')
    print('----------------------------')
    print LED.dictionary
    while True:
        result = activitycode(LED.dictionary)
        redLED.getstate
        yellowLED.getstate
        greenLED.getstate  
        if result == False:
            print "[--system--] powering down."
            bootseq(0,3)
            time.sleep(4)
            GPIO.cleanup()
            break


def bootseq(x,repeat):
    redLED.off
    greenLED.off
    yellowLED.off

    p_red= Thread(target = redLED.blink, args = (repeat,None))
    p_green= Thread(target = greenLED.blink, args = (repeat,None))
    p_yellow= Thread(target = yellowLED.blink, args = (repeat,None))
    if x:
        time.sleep(2)
        p_green.start()
        time.sleep(.25)
        p_yellow.start()
        time.sleep(.25)
        p_red.start()
    else:
        time.sleep(2)
        p_red.start()
        time.sleep(.25)
        p_yellow.start()
        time.sleep(.25)
        p_green.start()
 
 
 
 

########################  activityentered_code()  ###########################

def activitycode(choices):
    entered_code = [str(x) for x in raw_input('\n[--system--] enter code for LED behavior: LEDname on/off/blink..\n>>>').split()]
    for argument in entered_code:
        if argument in choices:
            behavior_choice_index = entered_code.index(argument)+1
            #print(argument, entered_code[behavior_choice_index])
            if entered_code[behavior_choice_index] == "on":
                choices[argument].on()
            elif entered_code[behavior_choice_index] == "off":
                choices[argument].off()
            elif entered_code[behavior_choice_index] == "blink":
                try:blinkrepeat = entered_code[behavior_choice_index + 1]
                except: blinkrepeat = None
                try:blinkspeed = entered_code[behavior_choice_index + 2]
                except: blinkspeed = None
                #background the call of LED.blink
                b1= Thread(target = choices[argument].blink, args = (blinkrepeat,blinkspeed))
                #choices[argument].blink(blinkrepeat,blinkspeed)
                b1.start()
        elif argument == "exit":
            return False

##############################################################################
#                       Executable code below:
##############################################################################

main()

