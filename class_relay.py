#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier                                  #
#   developed on: 04/10/2016                                        #
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

GPIO.setwarnings(False)      #set to false if the warnings bother you, helps troubleshooting


#####################################################################
#                           Classes
#####################################################################
class bcolors:                          #these are the color codes
    """
    Toggle switch for printing in color. Once activated, everything following is in color X

    This color class is completely unecessary, but it makes the output cooler, and doesn't really cause any harm
    if you remove it, you'll have to remove all uses of it in the functions
                        example:
    print(bcolors.YELLOW + "Warning" + bcolors.END)
    this prints "Warning" in yellow, then turns off colors, so everything printed after END will be normal
    """

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



##########################  LED class  #############################
class LED:
    """
    Turns GPIO pins from LOW(off) to HIGH(on) and back again

    this class pretty much works for any device connected to a single GPIO pin
    as instances of LED are created, their names are added as keys in the LED.dictionary
    """
    dictionary  = {}                #a dictionary will all created LED instances' names as keys
    #state = None
    def __init__(self,pin,name,color,power):
        self.pin = int(pin)         #this is the GPIO pin number (will depend on GPIO config)
        self.name = name
        self.color = color
        self.power = power          #enter power in miliamps
        self.state = GPIO.input(self.pin)           #was going to use conditional loop if I could have got backgrounding to work
        LED.dictionary[name] = self #auto adds every instance of LED to the dictionary

    def getstate(self):
        self.state = GPIO.input(self.pin)
        return self.state

    def fake(self):
        if GPIO.output(self.pin):           # if self.pin == 1  
            print "%s on port %s is 1/GPIO.HIGH/True"%(self.name,self.pin)
        else:
            print "%s on port %s is 0/GPIO.LOW/False"%(self.name,self.pin)

    def on(self):
        GPIO.output(self.pin,GPIO.HIGH)
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)

    def off(self):
        GPIO.output(self.pin,GPIO.LOW)
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)

    def blink(self, *args):
        #print (len(args))          #troubleshooting print statement
        #print args                 # another
        try:
            repeat= int(args[0])
        except: repeat = 1
        try:
                speed = (float(args[1]))/2
        except: speed = .5
        #print repeat               #troubleshooting print statement
        #print speed                # another
        print("%s LED is"%self.color + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        while repeat > 0:
            self.state = "blinking"
            GPIO.output(self.pin,GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(self.pin,GPIO.LOW)
            time.sleep(speed)
            repeat -= 1

#####################################################################
class Relay:
    """
    Turns GPIO pins from LOW(off) to HIGH(on) and back again

    this class pretty much works for any device connected to a single GPIO pin
    as instances of Relays are created, their names are added as keys in the Relay.dictionary
    """
    dictionary  = {}                #a dictionary will all created LED instances' names as keys
    #state = None
    def __init__(self,pin,name):
        self.pin = int(pin)         #this is the GPIO pin number (will depend on GPIO config)
        self.name = name
        self.state = GPIO.input(self.pin)           #was going to use conditional loop if I could have got backgrounding to work
        LED.dictionary[name] = self #auto adds every instance of LED to the dictionary

    def getstate(self):
        self.state = GPIO.input(self.pin)
        return self.state

    def fake(self):
        if GPIO.output(self.pin):           # if self.pin == 1  
            print "%s on port %s is 1/GPIO.HIGH/True"%(self.name,self.pin)
        else:
            print "%s on port %s is 0/GPIO.LOW/False"%(self.name,self.pin)

    def on(self):
        GPIO.output(self.pin,GPIO.LOW)
        print("%s Relay is"%self.name + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)

    def off(self):
        GPIO.output(self.pin,GPIO.HIGH)
        print("%s LED is"%self.name + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)

    def blink(self, *args):
        #print (len(args))          #troubleshooting print statement
        #print args                 # another
        try:
            repeat= int(args[0])
        except: repeat = 1
        try:
                speed = (float(args[1]))/2
        except: speed = .5
        #print repeat               #troubleshooting print statement
        #print speed                # another
        print("%s Relay is"%self.name + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        while repeat > 0:
            self.state = "blinking"
            GPIO.output(self.pin,GPIO.LOW)
            time.sleep(speed)
            GPIO.output(self.pin,GPIO.HIGH)
            time.sleep(speed)
            repeat -= 1

def main():
    """
    loop asking for an activity code via raw input. Exits by typing 'exit'
    """
    print('\n\n\n\n\n[--system--] enter code for behavior: LEDname on/off/strobe\n')
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
    print('     TEST MODE ACTIVATED    ')
    print('----------------------------')
    print LED.dictionary
    while True:
        result = activitycode(LED.dictionary)
        if result == False:
            print "[--system--] powering down."
            GPIO.cleanup()
            break


########################  activityentered_code()  ###########################

def activitycode(choices):
    entered_code = [str(x) for x in raw_input('\n[--system--] enter code for relay behavior: Relay name on/off/blink..\n>>>').split()]
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

if __name__ == '__main__':
    try:
        relaydict = {}
        while True:
            setpin = raw_input('Enter GPIO pin number, or enter "done" to begin testing. ')
            if str(setpin) == 'done':
                main()
                print '\n\nSet more pins, or ctr+c to shut down.'
            else: 
                GPIO.setup(int(setpin),GPIO.OUT, initial = 1)
                setname = raw_input('Name of this relay: ')
                relaydict[setname] = Relay(setpin,setname)
    
    except KeyboardInterrupt:
        print '\n\n\n[--system--] powering down.'
    finally:
        GPIO.cleanup()
        print "GPIO pins have been cleaned up.  Goodbye!"
