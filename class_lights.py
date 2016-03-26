#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier                                  #
#   developed on: 03/25/2016                                        #
#   contact:austinmeier on github                                   #
#####################################################################
"""


###########################  Imports here  ##########################

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

GPIO.setwarnings(True)      #set to false if the warnings bother you, helps troubleshooting

############################ Activating pins ########################
#GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)


########################### if pin is GPIO.OUT  ######################

#turning the pins on or off

#GPIO.output(18,GPIO.HIGH)   #on
#GPIO.output(18,GPIO.LOW)    #off


##########################  if pin is GPIO.IN  ########################




#####################################################################
#                           Classes
#####################################################################

class bcolors:                          #these are the color codes
    PURPLE = '\033[95m'                 #purple
    BLUE = '\033[94m'                   #blue
    GREEN = '\033[92m'                  #green
    YELLOW = '\033[93m'                 #yellow
    RED = '\033[91m'                    #red
    END = '\033[0m'                     #turns off color
    BOLD = '\033[1m'                    #turns on bold
    def disable(self):
        self.PURPLE = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.END = ''
        self.BOLD = ''

#example:
#print(bcolors.YELLOW + "Warning" + bcolors.END)
#  this prints "Warning" in yellow, then turns off colors, so everything printed after END will be normal




class LED:
    def __init__(self,pin,color,power):
        self.pin = int(pin)
        self.color = color
        self.power = power          #enter power in miliamps

    def on(self):
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)
        GPIO.output(self.pin,GPIO.HIGH)
        time.sleep(2) 
    def off(self):
        GPIO.output(self.pin,GPIO.LOW)
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)
    def blink(self):
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        GPIO.output(self.pin,GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(self.pin,GPIO.LOW)
        time.sleep(.5)


#####################################################################
greenLED= LED(17,"green", 20)
redLED= LED(27,"red", 20)
yellowLED= LED(18,"yellow", 20)



#####################################################################
#                     Put code below this
#####################################################################

def main():
    print('\n\n\n\n\n[--system--] enter code for LED behavior: LEDname on/off/strobe\n')
    print('\nconnecting....')
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
    while True:
        result = activitycode(['yes','maybe']) 
        if result == False:
            print "[--system--] powering down."
            redLED.blink()
            greenLED.blink()
            yellowLED.blink()
            time.sleep(2)
            GPIO.cleanup()
            break


########################  activitycode()  ###########################
def activitycode(choices):
    code = [str(x) for x in raw_input('\n[--system--] enter code for LED behavior: LEDname on/off/blink..\n>>>').split()]
    for argument in code:
        if argument in choices:
            behavior_choice = code.index(argument)+1
            print behavior_choice
        elif argument == "exit":
            return False

main()

"""

#Uncomment this whole set when you're ready to add the polish to the script
#it essentially just runs pin cleanup if for some reason the program freezes before it finishes
#I dont really understand it, but it came from this page: 
# http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi


try:  
    main()
    

    while True:
        redLED.on()
        time.sleep(1)
        redLED.off()
        time.sleep(1)
        redLED.blink()
    # here you put your main loop or block of code  
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


"""
