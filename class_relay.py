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

GPIO.cleanup()             #shouldn't need to use this, but just in case

GPIO.setwarnings(False)      #set to false if the warnings bother you, helps troubleshooting

############################ Activating pins ########################
#GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(21,GPIO.OUT, initial = 1)
GPIO.setup(19,GPIO.OUT, initial = 1)
#GPIO.setup(18,GPIO.OUT, initial = 1)


########################### if pin is GPIO.OUT  ######################

#turning the pins on or off

#GPIO.output(18,GPIO.HIGH)   #on
#GPIO.output(18,GPIO.LOW)    #off


##########################  if pin is GPIO.IN  ########################




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


#
#####################################################################
relay1 = Relay(21,"lights")
relay4 = Relay(19, "fans")
#####################################################################
#                     Put code below this
#####################################################################

def main():
    """
    loop asking for an activity code via raw input. Exits by typing 'exit'
    """
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
    print LED.dictionary
    while True:
        result = activitycode(LED.dictionary)
        relay1.getstate
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
