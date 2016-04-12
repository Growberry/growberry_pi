#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier
#   developed on: 04/10/16                                          #
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

#Examples:
GPIO.setup(21,GPIO.OUT, initial = GPIO.LOW)
#GPIO.setup(27,GPIO.IN)
#GPIO.setup(18,GPIO.OUT)


########################### if pin is GPIO.OUT  ######################

#turning the pins on or off

#GPIO.output(18,GPIO.HIGH)   #on
#GPIO.output(18,GPIO.LOW)    #off


##########################  if pin is GPIO.IN  ########################




#####################################################################
#                           Classes
#####################################################################



#####################################################################


#####################################################################
#                     Put code below this
#####################################################################
for x in range(0,3):
    GPIO.output(21,GPIO.HIGH)   #on
    print("Light on")
    time.sleep(3)
    GPIO.output(21,GPIO.LOW)
    print("Light off")
    time.sleep(3)

GPIO.cleanup()
"""

#Uncomment this whole set when you're ready to add the polish to the script
#it essentially just runs pin cleanup if for some reason the program freezes before it finishes
#I dont really understand it, but it came from this page: 
# http://raspi.tv/2013/rpi-gpio-basics-3-how-to-exit-gpio-programs-cleanly-avoid-warnings-and-protect-your-pi


try:  
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

