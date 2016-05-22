
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

##########################  Relay class ##############################
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
        Relay.dictionary[name] = self #auto adds every instance of Relay to the dictionary

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


#######
class Config:
    """
    reads config file, and modifies it
    """
    dictionary  = {}                #a dictionary will all created config instances' names as keys
    #state = None
    def __init__(self,path,name):
        cfg.read(path)
        self.path = path
        self.sections =  cfg.sections()         # this is the sections in your config file (usually in a bracket)
        self.name = name                        # here mostly so something can be added to the config.dict
        Config.dictionary[name] = self          # auto adds every instance of config to the dictionary
        self.settings = {}

        cfg.read(path)
        ### *** READ config file ***
        cfg.read('config.ini')

        # Read interval
        self.settings['measurement_interval'] = cfg.get('options', 'measurement_interval')

        # LIGHTS ON TIME
        self.settings['lights_on_time'] = cfg.get('options', 'lights_on_time')

        # Length of day (in hours)
        self.settings['daylength'] = cfg.get('options', 'daylength')

        # TEMP that activates fans
        self.settings['fan_temp'] = cfg.get('options', 'fan_temp')

        # times that the sprinkler should run (list of strings)
        self.settings['watertimes'] = cfg.get('options', 'watertimes').split(',')

        # length of sprinkler cycle (in minutes)
        self.settings['pumptime'] = cfg.get('options', 'pumptime')

        # toggle picture capture on/off
        self.settings['toggle_camera'] = cfg.get('options', 'toggle_camera')

        # file to write the log file to
        self.settings['logfile'] = cfg.get('options', 'logfile')

        # directory to save pictures in
        self.settings['pic_dir'] = cfg.get('options', 'pic_dir')


    def source(self):
        cfg.read(self.path)
        ### *** READ config file ***
        cfg.read('config.ini')
        self.settings['measurement_interval'] = cfg.get('options', 'measurement_interval')
        self.settings['lights_on_time'] = cfg.get('options', 'lights_on_time')
        self.settings['daylength'] = cfg.get('options', 'daylength')
        self.settings['fan_temp'] = cfg.get('options', 'fan_temp')
        self.settings['watertimes'] = cfg.get('options', 'watertimes').split(',')
        self.settings['pumptime'] = cfg.get('options', 'pumptime')
        self.settings['toggle_camera'] = cfg.get('options', 'toggle_camera')
        self.settings['logfile'] = cfg.get('options', 'logfile')
        self.settings['pic_dir'] = cfg.get('options', 'pic_dir')

        return self.settings

    def change(self, setting, new):
        cfg['options'][setting] = new  # set "string"
        with open('config.ini', 'w') as configfile:
            cfg.write(configfile)
            self.source()
            print('The new %s is %s'%(setting, self.settings[setting]))



#####################################################################
relay1 = Relay(12,"water")
relay4 = Relay(19, "fans")
growsettings = Config('config.ini',"grow")
#####################################################################

#####################################################################
#                       Functions
#####################################################################

def importconfig(configfile):
    config_dict = {}
    ### *** READ config file ***
    cfg.read(configfile)

    config_dict['measurement_interval'] = cfg.getfloat('options', 'measurement_interval')

    # LIGHTS ON TIME
    config_dict['lights_on_time'] = cfg.get('options', 'lights_on_time')

    # Length of day (in hours)
    config_dict['daylength'] = cfg.getfloat('options', 'daylength')

    # TEMP that activates fans
    config_dict['fan_temp'] = cfg.getfloat('options', 'fan_temp')

    # times that the sprinkler should run (list of strings)
    config_dict['watertimes'] = cfg.get('options', 'watertimes').split(',')

    # length of sprinkler cycle (in minutes)
    config_dict['pumptime'] = cfg.getfloat('options', 'pumptime')

    # toggle picture capture on/off
    config_dict['toggle_camera'] = cfg.getboolean('options', 'toggle_camera')

    # file to write the log file to
    config_dict['logfile'] = cfg.get('options', 'logfile')

    # directory to save pictures in
    config_dict['pic_dir'] = cfg.get('options', 'pic_dir')

    return config_dict

########################  activityentered_code()  ###########################
def activitycode(choices,config):
    """
    In manual mode, you can enter a string, split into arguments at each space.
    Each argument is checked against the list of possible choices, and if the argument is in the list,
    the argument immediately following will dictate the behavior
    """
    entered_code = [str(x) for x in
                    raw_input('\n[--system--] enter code for relay behavior:\n>>>').split()]
    for argument in entered_code:
        if argument in choices:
            print "relay selected - would normally activate selected relay"
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
        elif argument in config.settings:
            newsettingindex = entered_code.index(argument) + 1
            config.change(argument,entered_code[newsettingindex])

        elif argument == "exit":
            return False





#####################################################################
#                            MAIN
#####################################################################


def main():
    """
    loop asking for an activity code via raw input. Exits by typing 'exit'
    """

    print('\n\n\n\n\n')

    print(bcolors.RED + bcolors.BOLD +
        '  ________                    ___.                                                 \n'+\
        ' /  _____/______  ______  _  _\_ |__   __________________ ___.__.    ______ ___.__.\n'+bcolors.YELLOW +\
        '/   \  __\_  __ \/  _ \ \/ \/ /| __ \_/ __ \_  __ \_  __ \   |  |    \____ \   |  |\n'+\
        '\    \_\  \  | \(  <_> )     / | \_\ \  ___/|  | \/|  | \/\___  |    |  |_> >___  |\n'+bcolors.GREEN +\
        ' \______  /__|   \____/ \/\_/  |___  /\___  >__|   |__|   / ____| /\ |   __// ____|\n'+\
        '        \/                         \/     \/              \/      \/ |__|   \/     \n'+bcolors.END)
    global last_water
    try:
        logfile = cfg.get('options', 'logfile').replace("'", "")  # get "string" object
        lastlog = subprocess.check_output(['tail', '-1', logfile])
    except:
        # if that doesn't work, just print this warning
        lastlog = "Could not retrieve last status"

    print lastlog

    while True:
        result = activitycode(Relay.dictionary,growsettings)
        if result == False:
            print "[--system--] powering down."
            GPIO.cleanup()
            break




##############################################################################
#                       Executable code below:
##############################################################################

try:
    main()
except KeyboardInterrupt:
    print "Goodbye!"
finally:
    GPIO.cleanup()



