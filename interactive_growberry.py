
#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier                                  #
#   developed on: 05/21/2016                                        #
#   contact:austinmeier on github                                   #
#####################################################################
"""


###########################  Imports here  ##########################
from threading import Thread
import time
import os
from time import sleep
import RPi.GPIO as GPIO
import subprocess
from configparser import ConfigParser
cfg = ConfigParser()



#####################################################################
#                           GPIO pin set up
#####################################################################
#select one of these two modes:
GPIO.setmode(GPIO.BCM)      #for using the names of the pins

GPIO.setwarnings(True)      #This should alert you to the fact that growberry_.py is already using the pins

############################ Activating pins ########################
#GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for relays

GPIO.setup(19,GPIO.OUT, initial = 1)
GPIO.setup(12,GPIO.OUT, initial = 1)



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
relay1 = Relay(12,"water")
relay4 = Relay(19, "fans")
#####################################################################
#                     Put code below this
#####################################################################


#####################################################################
#                       Functions
#####################################################################

def current_config():
    ### *** READ config file ***
    cfg.read('config.ini')

    # Read interval
    measurement_interval = cfg.getfloat('general', 'measurement_interval')

    # LIGHTS ON TIME
    lights_on_time = cfg.get('lights', 'lights_on_time')

    # Length of day (in hours)
    daylength = cfg.getfloat('lights', 'daylength')

    # TEMP that activates fans
    fan_temp = cfg.getfloat('general', 'fan_temp')

    # times that the sprinkler should run (list of strings)
    watertimes = cfg.get('irrigation', 'watertimes')

    # length of sprinkler cycle (in minutes)
    pumptime = cfg.getfloat('irrigation', 'pumptime')

    # toggle picture capture on/off
    toggle_camera = cfg.getboolean('general', 'toggle_camera')

    # file to write the log file to
    logfile = cfg.get('io', 'logfile')

    # directory to save pictures in
    pic_dir = cfg.get('io', 'pic_dir')

    print(
        "The measurement interval is: ",measurement_interval,"\n",
        "The lights will turn on for ",daylength, " beginning at ", lights_on_time,"\n",
        "If the temperature exceeds ",fan_temp," degrees celcius, the fans will be activated\n",
        "The waterpump with be activated for ",pumptime," minutes at these times: ",watertimes,"\n",
        "The camera is toggled on: ",toggle_camera,"\n",
        "If 'True', the resulting pictures will be saved in ",pic_dir,"\n",
        "All data is logged to ",logfile,"\n",
        )

    print(cfg.sections())       # return all sections
    print(cfg.items('io')) # return section's list
    print(cfg.get('io', 'logfile'))
    print(cfg.getfloat('general', 'fan_temp'))
    print(cfg.get('configData1', 'conf2'))
    print(cfg.get('configData1', 'conf3'))

    print(cfg.get('configData2', 'config_string'))  # get "string" object
    print(cfg.getboolean('configData2', 'config_bool')) # get "bool" object
    print(cfg.getint('configData2', 'config_int'))      # get "int" object
    print(cfg.getfloat('configData2', 'config_float'))  # get "float" object
    try:
        logfile = cfg.get('io', 'logfile').replace("'", "")  # get "string" object
        lastlog = subprocess.check_output(['tail', '-1', logfile])
    except:
        # if that doesn't work, just print this warning
        lastlog = "Could not retrieve last status"

    print lastlog











def main():
    """
    loop asking for an activity code via raw input. Exits by typing 'exit'
    """

    print('\n\n\n\n\n')

    print(bcolors.RED + bcolors.BOLD +
        '  ________                    ___.                                                 \n'+\
        ' /  _____/______  ______  _  _\_ |__   __________________ ___.__.    ______ ___.__.\n'+bcolors.YELLOW +\
        '/   \  __\_  __ \/  _ \ \/ \/ /| __ \_/ __ \_  __ \_  __ <   |  |    \____ <   |  |\n'+\
        '\    \_\  \  | \(  <_> )     / | \_\ \  ___/|  | \/|  | \/\___  |    |  |_> >___  |\n'+bcolors.GREEN +\
        ' \______  /__|   \____/ \/\_/  |___  /\___  >__|   |__|   / ____| /\ |   __// ____|\n'+\
        '        \/                         \/     \/              \/      \/ |__|   \/     \n'+bcolors.END)
    global last_water

    current_config()
    #activitycode(LED.dictionary)


########################  activityentered_code()  ###########################

def activitycode(choices):
    """
    In manual mode, you can enter a string, split into arguments at each space.
    Each argument is checked against the list of possible choices, and if the argument is in the list,
    the argument immediately following will dictate the behavior
    """
    entered_code = [str(x) for x in
                    raw_input('\n[--system--] enter code for relay behavior: Relay name (%s) on/off/blink..\n>>>'%choices).split()]
    for argument in entered_code:
        if argument in choices:
            behavior_choice_index = entered_code.index(argument) + 1
            # print(argument, entered_code[behavior_choice_index])
            if entered_code[behavior_choice_index] == "on":
                choices[argument].on()
            elif entered_code[behavior_choice_index] == "off":
                choices[argument].off()
            elif entered_code[behavior_choice_index] == "blink":
                try:
                    blinkrepeat = entered_code[behavior_choice_index + 1]
                except:
                    blinkrepeat = None
                try:
                    blinkspeed = entered_code[behavior_choice_index + 2]
                except:
                    blinkspeed = None
                # background the call of LED.blink
                b1 = Thread(target=choices[argument].blink, args=(blinkrepeat, blinkspeed))
                # choices[argument].blink(blinkrepeat,blinkspeed)
                b1.start()
        elif argument == "exit":
            return False


##############################################################################
#                       Executable code below:
##############################################################################

try:
    main()

except KeyboardInterrupt:
    print "Goodbye!"
finally:
    GPIO.cleanup()
#!/usr/bin/env python


