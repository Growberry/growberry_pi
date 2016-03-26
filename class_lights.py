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

#GPIO.cleanup()             #shouldn't need to use this, but just in case

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

class LED:
    def __init__(self,pin,color,power):
        self.pin = int(pin)
        self.color = color
        self.power = power          #enter power in miliamps

    def on(self):
        print("%s LED is on."%self.color)
        GPIO.output(self.pin,GPIO.HIGH)
        time.sleep(2) 
    def off(self):
        GPIO.output(self.pin,GPIO.LOW)
        print("%s LED is off."%self.color)
   
#####################################################################


#####################################################################
#                     Put code below this
#####################################################################


greenLED= LED(17,"green", 20)
redLED= LED(27,"red", 20)
yellowLED= LED(18,"yellow", 20)




#Uncomment this whole set when you're ready to add the polish to the script
#it essentially just runs pin cleanup if for some reason the program freezes before it finishes
#I dont really understand it, but it came from this page: 
# http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi


try:  

    while True:
        greenLED.on()
        time.sleep(5)
        greenLED.off()
        time.sleep(5)
        #greenLED.on()
        #yellowLED.on()

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



