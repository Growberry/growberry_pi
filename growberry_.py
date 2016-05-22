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
import os
import datetime
from threading import Thread
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
from picamera import PiCamera
import subprocess
from configparser import ConfigParser
cfg = ConfigParser()
#####################################################################
#                           Parameters
#####################################################################
# # Change these things to change how the threasholds work
#
# # Read interval
# measurement_interval = 10.00
#
# # LIGHTS ON TIME
# lights_on_time = '1100'
#
# # Length of day (in hours)
# daylength = 12
#
# # TEMP that activates fans
# fan_temp = 22.5
#
# # times that the sprinkler should run (list of strings)
# watertimes = ['0600','1100','1600','2100']
#
# # length of sprinkler cycle (in minutes)
# pumptime = 3
#
# # toggle picture capture on/off
# toggle_camera = True
#
# # file to write the log file to
# logfile = '/home/pi/usbdrv/growberry_testlog/grow1_log.txt'
#
# # directory to save pictures in
# pic_dir = '/home/pi/usbdrv/growberry_testlog/flowering_pictures/'
#

growsettings = {}


#####################################################################
#                           GPIO pin set up
#####################################################################
# select one of these two modes:
GPIO.setmode(GPIO.BCM)  # for using the names of the pins

GPIO.setwarnings(True)  # set to false if the warnings bother you, helps troubleshooting

############################ Activating pins ########################
# GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(12, GPIO.OUT, initial=1)
GPIO.setup(19, GPIO.OUT, initial=1)
#fake pin setup to use while testing the sprinkler
GPIO.setup(21, GPIO.OUT, initial=1)

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


class Relay:
    """
    Turns GPIO pins from LOW(on) to HIGH(off) and back again.  Remember: relays are inverted. 
    3.3v turns the relay off.

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
        #print("%s Relay is" % self.name + bcolors.BOLD + bcolors.GREEN + " on." + bcolors.END)

    def off(self):
        """
        switches GPIO pin to HIGH/1 - in open state relays, this turns the relay OFF.
        """
        GPIO.output(self.pin, GPIO.HIGH)
        #print("%s Relay is" % self.name + bcolors.BOLD + bcolors.RED + " off." + bcolors.END)

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

        #print 'Temperature: {0:0.1f} C'.format(temp)       #prints Temp formated
        #print 'Humidity:    {0:0.1f} %'.format(humidity)   #prints Humidity formatted

        #print temp         #prints temp unformated
        #print humidity     #prints humidity unformated

        # Sometimes the sensor will return "None"
        # This might happen if the CPU is under a lot of load and the sensor$
        # can't be reliably read (timing is critical to read the sensor).$
        # the following loop will read the sensor every 2 seconds until both temp and humidity are not "None"

        while humidity is None or temp is None:  #this should prevent errors when rounding, but could cause a hang-up...
            time.sleep(2)
            humidity, temp = Adafruit_DHT.read(self.sens_type, self.pin)

        return {"temp": round(float(temp),1), "humidity": round(float(humidity),1), "timestamp": datetime.datetime.now()}


############### Define things controlled vi Pi #####################
####################### GLOBAL VARIABLES  ##########################
#lights currently controled via timer so I can test the water pump needs to go back to the correct pin
LIGHTS = Relay(21, "lights")

FANS = Relay(19, "fans")

H2O_PUMP = Relay(12, "water pump")
last_water = "not watered yet"
sensor1 = Sensor(17, Adafruit_DHT.DHT22, "temp_humidity")



#####################################################################
#                           FUNCTIONS
#####################################################################
# worksheet.append_row((datetime.datetime.now(),time.strftime('%m/%d/%Y'),time.strftime("%H:%M:%S"), temp, humidity))$

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


def takepic(save_dir):
    """Take a picture, and save it to directory specified using the date.time as the name"""
    timestamp = time.strftime("%Y-%m-%d.%H%M")
    camera.capture('%s%s.jpg'%(save_dir, timestamp))

def watercycle(pumptime):
    """ turns water pump on for time specified (in minutes)"""
    global last_water
    H2O_PUMP.on()
    time.sleep(pumptime*60)
    H2O_PUMP.off()
    last_water = datetime.datetime.now()

def sprinkler(growsettings):
    """checks if the sprinkler needs to run, returns the time since the end of the last watercycle run"""

    #set up the watering cycle function to be started as a second thread and to run for the pump time
    pumptime = growsettings['pumptime']
    w1 = Thread(target=watercycle, args=(pumptime,))

    if last_water != "not watered yet":
        timesinceH2O = datetime.datetime.now() - last_water
    else:
        timesinceH2O = last_water

    for lime in growsettings['watertimes']:
        # convert the scheduled watertime to a date.time and see if it falls in the previous measurment_interval.
        # if yes, start the watercylce
        x = datetime.datetime.strptime(lime, '%H%M').time()
        H2Otime = datetime.datetime.combine(datetime.date.today(), x)
        if (datetime.datetime.now() - datetime.timedelta(minutes= growsettings['measurement_interval'])) <= H2Otime <= datetime.datetime.now():
            w1.start()

    return timesinceH2O

def lightcontrol(t, daylength):
    """send in the time to turn the lights on, and how long to keep them on for. Returns a light status"""

    i = datetime.datetime.strptime(t, '%H%M').time()

    ontime = datetime.datetime.combine(datetime.date.today(), i)
    offtime = ontime + datetime.timedelta(hours=daylength)

    if ontime <= datetime.datetime.now() <= offtime:
        LIGHTS.on()
        return "Lights:ON"
    else:
        LIGHTS.off()
        return "Lights:OFF"

def growmonitor():
    """
    Every interval minutes, read the temp/humidity, if temp exceeds set_temp, turn on fans, 
    if time falls between set_time1 and set_time2: turn light on
    """

    last_water = None
    fan_status = None
    while True:
        #update the settings
        growsettings = importconfig('config.ini')
        #take picture and write it to the pic directory
        if growsettings['toggle_camera']:
            takepic(growsettings['pic_dir'])
        # read the sensor, check temp, turn fans on/off
        sensor_reading = sensor1.read()  # returns a dictionary with "temp", "humidity", and "timestamp" keys
        if sensor_reading["temp"] > float(growsettings['fan_temp']):
            fan_status = "Fans:ON"
            FANS.on()
        else:
            fan_status = "Fans:OFF"
            FANS.off()

        #run lightcontrol, which takes a time to turn on, and a "daylength"
        light_status = lightcontrol(growsettings['lights_on_time'], growsettings['daylength'])

        tslw = sprinkler(growsettings['measurement_interval'])
        timesincelastwater = str(tslw)

        data_line = (str(sensor_reading["timestamp"]), str(time.strftime("%Y-%m-%d.%H%M")), str(sensor_reading["temp"]), str(sensor_reading["humidity"]), light_status, fan_status, timesincelastwater, '\n')



        print_light_status = None
        if light_status.split(':')[1]== "ON":
            print_light_status = "Lights:"+ bcolors.GREEN + 'ON' +bcolors.END
        elif light_status.split(':')[1]== "OFF":
            print_light_status = "Lights:"+ bcolors.RED + 'OFF' +bcolors.END

        print_fan_status = None
        if fan_status.split(':')[1]== "ON":
            print_fan_status = "Fans:"+ bcolors.GREEN + 'ON' +bcolors.END
        elif fan_status.split(':')[1]== "OFF":
            print_fan_status = "Fans:"+ bcolors.RED + 'OFF' +bcolors.END

        print(str(sensor_reading["timestamp"])+'\t'+ str(time.strftime("%Y-%m-%d.%H%M")) +'\t'+ str(sensor_reading["temp"]) +'\t'+ str(sensor_reading["humidity"]) +'\t'+ print_light_status +'\t'+ print_fan_status + '\tTimeSinceWater:'+timesincelastwater )

        with open(growsettings['logfile'], "a") as data_log:
            #write the data line in TSV format
            data_log.write("\t".join(data_line))

        time.sleep(growsettings['measurement_interval'] * 60)


def main():
    growsettings = importconfig('config.ini')
    print('\n\n\n\n\n')

    print(bcolors.RED + bcolors.BOLD +
        '  ________                    ___.                                                 \n'+\
        ' /  _____/______  ______  _  _\_ |__   __________________ ___.__.    ______ ___.__.\n'+bcolors.YELLOW +\
        '/   \  __\_  __ \/  _ \ \/ \/ /| __ \_/ __ \_  __ \_  __ <   |  |    \____ <   |  |\n'+\
        '\    \_\  \  | \(  <_> )     / | \_\ \  ___/|  | \/|  | \/\___  |    |  |_> >___  |\n'+bcolors.GREEN +\
        ' \______  /__|   \____/ \/\_/  |___  /\___  >__|   |__|   / ____| /\ |   __// ____|\n'+\
        '        \/                         \/     \/              \/      \/ |__|   \/     \n'+bcolors.END)
    global last_water
    try:
        # attempt to determine the time since last watering by reading the last line in the logfile
        line = subprocess.check_output(['tail', '-1', growsettings['logfile']])
        x = line.split('\t')
        last_log_time = datetime.datetime.strptime(x[1], "%Y-%m-%d.%H%M")
        t= datetime.datetime.strptime(x[6].split('.')[0], "%H:%M:%S")
        timesincewaterlastlog = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        last_water = last_log_time - timesincewaterlastlog
    except:
        # if that doesn't work, just use the default
        last_water = "not watered yet"


    growmonitor()



##############################################################################
#                       Executable code below:
##############################################################################

try:
    # camera is on by default, but in some cases toggling it off results in no camera initiation
    growsettings = importconfig('config.ini')
    if growsettings['toggle_camera']:
        camera = PiCamera()
    main()

except KeyboardInterrupt:
    print "Goodbye!"
finally:
    GPIO.cleanup()

