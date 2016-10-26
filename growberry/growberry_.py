#!/usr/bin/env python2.7
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

#self imports
from pins import Relay, Sensor


#####################################################################
#                       Global variables
#####################################################################


settings = {}

PIC_DIR =

#####################################################################
#                           GPIO pin set up
#####################################################################
"""These have also moved into pins.py"""

############################ Activating pins ########################
# GPIO.setup(<put pin number here>,GPIO.IN/OUT)  #will depend on setmode above, use "IN" for sensors, and "OUT" for LEDs

GPIO.setup(12, GPIO.OUT, initial=1)
GPIO.setup(19, GPIO.OUT, initial=1)
#fake pin setup to use while testing the sprinkler
GPIO.setup(21, GPIO.OUT, initial=1)

#####################################################################
#                           Classes
#####################################################################
"""These have been moved to the pins.py to clean up the code."""




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

    w1 = Thread(target=watercycle, args=(growsettings['pumptime'],))

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
        #else H2O_PUMP.off()
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
    global growsettings
    last_water = None
    fan_status = None
    while True:
        #update the settings
        growsettings = importconfig('/home/pi/Documents/git/growberry_pi/config.ini')
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

        tslw = sprinkler(growsettings)
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
    global growsettings
    growsettings = importconfig('/home/pi/Documents/git/growberry_pi/config.ini')
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
    global growsettings
    growsettings = importconfig('/home/pi/Documents/git/growberry_pi/config.ini')
    if growsettings['toggle_camera']:
        camera = PiCamera()
    main()

except KeyboardInterrupt:
    print "Goodbye!"
finally:
    GPIO.cleanup()

