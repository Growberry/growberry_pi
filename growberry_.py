#!/usr/bin/env python
"""
#####################################################################
#   code developed by: austinmeier                                  #
#   developed on: 04/10/2016                                        #
#   contact:austinmeier on github                                   #
#####################################################################
"""

###########################  Imports here  ##########################


# from datetime import datetime, time
import datetime
from threading import Thread
import time
import os
import RPi.GPIO as GPIO
import Adafruit_DHT
from picamera import PiCamera

#####################################################################
#                           GPIO pin set up
#####################################################################
# select one of these two modes:
GPIO.setmode(GPIO.BCM)  # for using the names of the pins
# or
# GPIO.setmode(GPIO.BOARD)   #for true pin number IDs (pin1 = 1)

GPIO.cleanup()  # shouldn't need to use this, but just in case

GPIO.setwarnings(False)  # set to false if the warnings bother you, helps troubleshooting

############################ Activating pins ########################
# GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(21, GPIO.OUT, initial=1)
GPIO.setup(19, GPIO.OUT, initial=1)


# GPIO.setup(17,GPIO.OUT, initial = 1)


#####################################################################
#                           Classes
#####################################################################
class bcolors:  # these are the color codes
    """
    Toggle switch for printing in color. Once activated, everything following is in color X

    This color class is completely unecessary, but it makes the output cooler, and doesn't really cause any harm
    if you remove it, you'll have to remove all uses of it in the functions
                        example:
    print(bcolors.YELLOW + "Warning" + bcolors.END)
    this prints "Warning" in yellow, then turns off colors, so everything printed after END will be normal
    """

    PURPLE = '\033[95m'  # purple
    BLUE = '\033[94m'  # blue
    GREEN = '\033[92m'  # green
    YELLOW = '\033[93m'  # yellow
    RED = '\033[91m'  # red
    END = '\033[0m'  # turns off color
    BOLD = '\033[1m'  # turns on bold

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
    dictionary = {}  # a dictionary will all created LED instances' names as keys

    # state = None
    def __init__(self, pin, name, color, power):
        self.pin = int(pin)  # this is the GPIO pin number (will depend on GPIO config)
        self.name = name
        self.color = color
        self.power = power  # enter power in miliamps
        self.state = GPIO.input(self.pin)  # was going to use conditional loop if I could have got backgrounding to work
        LED.dictionary[name] = self  # auto adds every instance of LED to the dictionary

    def getstate(self):
        self.state = GPIO.input(self.pin)
        return self.state

    def fake(self):
        if GPIO.output(self.pin):  # if self.pin == 1
            print "%s on port %s is 1/GPIO.HIGH/True" % (self.name, self.pin)
        else:
            print "%s on port %s is 0/GPIO.LOW/False" % (self.name, self.pin)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("%s LED is" % self.color + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("%s LED is" % self.color + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)

    def blink(self, *args):
        # print (len(args))          #troubleshooting print statement
        # print args                 # another
        try:
            repeat = int(args[0])
        except:
            repeat = 1
        try:
            speed = (float(args[1])) / 2
        except:
            speed = .5
        # print repeat               #troubleshooting print statement
        # print speed                # another
        print("%s LED is" % self.color + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        while repeat > 0:
            self.state = "blinking"
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(speed)
            repeat -= 1


#####################################################################
class Relay:
    """
    Turns GPIO pins from LOW(off) to HIGH(on) and back again

    this class pretty much works for any device connected to a single GPIO pin
    as instances of Relays are created, their names are added as keys in the Relay.dictionary
    """
    dictionary = {}  # a dictionary will all created LED instances' names as keys

    # state = None
    def __init__(self, pin, name):
        self.pin = int(pin)  # this is the GPIO pin number (will depend on GPIO config)
        self.name = name
        self.state = GPIO.input(self.pin)  # was going to use conditional loop if I could have got backgrounding to work
        LED.dictionary[name] = self  # auto adds every instance of LED to the dictionary

    def getstate(self):
        self.state = GPIO.input(self.pin)
        return self.state

    def fake(self):
        if GPIO.output(self.pin):  # if self.pin == 1
            print "%s on port %s is 1/GPIO.HIGH/True" % (self.name, self.pin)
        else:
            print "%s on port %s is 0/GPIO.LOW/False" % (self.name, self.pin)

    def on(self):
        """
        switches GPIO pin to LOW/0 - in open state relays, this turns the relay ON.
        """
        GPIO.output(self.pin, GPIO.LOW)
        print("%s Relay is" % self.name + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)

    def off(self):
        """
        switches GPIO pin to HIGH/1 - in open state relays, this turns the relay OFF.
        """
        GPIO.output(self.pin, GPIO.HIGH)
        print("%s LED is" % self.name + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)

    def blink(self, *args):
        # print (len(args))          #troubleshooting print statement
        # print args                 # another
        try:
            repeat = int(args[0])
        except:
            repeat = 1
        try:
            speed = (float(args[1])) / 2
        except:
            speed = .5
        # print repeat               #troubleshooting print statement
        # print speed                # another
        print("%s Relay is" % self.name + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        while repeat > 0:
            self.state = "blinking"
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(speed)
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(speed)
            repeat -= 1


class Sensor:
    def __init__(self, pin, sens_type, name):
        self.sens_type = sens_type
        self.pin = int(pin)  # this is the GPIO pin number (will depend on GPIO config)$
        self.name = name  #

    def read(self):
        humidity, temp = Adafruit_DHT.read(self.sens_type, self.pin)

        #print 'Temperature: {0:0.1f} C'.format(temp)
        #print 'Humidity:    {0:0.1f} %'.format(humidity)

        #print temp
        #print humidity

        # Skip to the next reading if a valid measurement couldn't be taken.$
        # This might happen if the CPU is under a lot of load and the sensor$
        # can't be reliably read (timing is critical to read the sensor).$

        if humidity is None or temp is None:
            time.sleep(2)
            humidity, temp = Adafruit_DHT.read(self.sens_type, self.pin)
        return {"temp": temp, "humidity": humidity, "timestamp": datetime.datetime.now()}


############### Define things controlled vi Pi #####################
LIGHTS = Relay(21, "lights")
FANS = Relay(19, "fans")
sensor1 = Sensor(17, Adafruit_DHT.DHT22, "temp_humidity")

camera = PiCamera()


#####################################################################
#                           FUNCTIONS
#####################################################################
# worksheet.append_row((datetime.datetime.now(),time.strftime('%m/%d/%Y'),time.strftime("%H:%M:%S"), temp, humidity))$

def takepic(save_dir):
    timestamp = time.strftime("%m%d%Y.%H%M")
    camera.capture('%s%s.jpg'%(save_dir, timestamp))




def growmonitor(interval, set_temp, set_hour1, set_min1, set_hour2, set_min2):
    """
    Every interval minutes, read the temp/humidity, if temp exceeds set_temp, turn on fans, 
    if time falls between set_time1 and set_time2: turn light on
    """
    fan_status = None
    light_status = None
    while True:
        # read the sensor, check temp, turn fans on/off
        sensor_reading = sensor1.read()  # returns a dictionary with "temp", "humidity", and "timestamp" keys
        if sensor_reading["temp"] > float(set_temp):
            fan_status = "Fans: on"
            FANS.on()
        else:
            fan_status = "Fans: off"
            FANS.off()
        # check if the time in within the set_times
        ontime = datetime.time(set_hour1, set_min1)
        offtime = datetime.time(int(set_hour2), int(set_min2))
        now = datetime.datetime.now()
        if ontime <= now.time() <= offtime:
            light_status = "Lights: on"
            LIGHTS.on()
        else:
            light_status = "Lights: off"
            LIGHTS.off()
        # print a data line
        data_line = (
        sensor_reading["timestamp"],time.strftime("%m-%d-%Y.%H%M"), sensor_reading["temp"], sensor_reading["humidity"], light_status, fan_status)
        print data_line
        time.sleep(interval * 60)


def main():
    print('\n\n\n\n\n')
    print('\nconnecting....')
    time.sleep(.2)
    print('....')
    time.sleep(.2)
    print('....')
    time.sleep(1)
    print('....')
    time.sleep(.5)
    print(
        '  ________                    ___.                                                 \n'+\
        ' /  _____/______  ______  _  _\_ |__   __________________ ___.__.    ______ ___.__.\n'+\
        '/   \  __\_  __ \/  _ \ \/ \/ /| __ \_/ __ \_  __ \_  __ <   |  |    \____ <   |  |\n'+\
        '\    \_\  \  | \(  <_> )     / | \_\ \  ___/|  | \/|  | \/\___  |    |  |_> >___  |\n'+\
        ' \______  /__|   \____/ \/\_/  |___  /\___  >__|   |__|   / ____| /\ |   __// ____|\n'+\
        '        \/                         \/     \/              \/      \/ |__|   \/     \n')

    growmonitor(2, 24, 7, 00, 23, 00)


########################  activityentered_code()  ###########################

def activitycode(choices):
    """
    In manual mode, you can enter a string, split into arguments at each space.
    Each argument is checked against the list of possible choices, and if the argument is in the list,
    the argument immediately following will dictate the behavior
    """
    entered_code = [str(x) for x in
                    raw_input('\n[--system--] enter code for relay behavior: Relay name on/off/blink..\n>>>').split()]
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

main()

