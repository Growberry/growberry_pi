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
#                     Put code below this
#####################################################################
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
print('Lights ON')
GPIO.output(17,GPIO.HIGH)
GPIO.output(27,GPIO.HIGH)

