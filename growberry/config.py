import os
import logging

# Set the base directory as the path of this file
basedir = os.path.abspath(os.path.dirname(__file__))

# A list containing all DH22 temp/humidity sensors
# if you add others, you need to set them up in __main__.py
# Names of 'internal' and 'external' must stay that way.
DHT22 = [ #(pin number, 'name')
    (17, 'internal'),
#    (22,'external')
]

#TODO: Overhaul the sensor opperation to accept different types of sensors within the predetermined locations/types
"""
while configuring, you will need to specify if you have sensors in these positions.  Use the format:
['type', pin]

heatsink sensors configured elsewhere
"""
acceptable_temp_types = ['DHT22']
acceptable_humidity_types = ['DHT22']

SENSORS = {
    'temp_sensors': {
        'internal':['DHT22',17],
        'external': None,
        'canopy': None
    },
    'humidity_sensors': {
        'internal': ['DHT22', 17],
        'external': None,
        'canopy': None
    },
}


LIGHTS = [19]  # if using binary lights (without PWM dimming)
# LIGHTS = [22, 5]  # use this line for [power pin, pwm pin]

# FANS = [13]  # if using a binary fan (without PWM speed control)
FANS = [13,18]  # Fans power pin, and PWM speed pin

# This switch allows you to put temp sensors on the heatsinks that will auto shut off lights if the temp is too hot.
HEATSINK_SAFETY = False
# Maximum temp for heatsinks before safetycheck shuts the lights off
MAXTEMP = 50

# If connected to a Growberry_web config, place the settings endpoint
SETTINGS_URL = 'http://192.168.0.42:8000/get_settings/'
#SETTINGS_URL = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/get_settings/'

# Find the settings.json file (this will get updated via request if online, or manually, if needed)
SETTINGS_JSON = os.path.join(basedir,'settings.json')

# data posting API
#DATAPOST_URL = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/reading/'
DATAPOST_URL = 'http://192.168.0.42:8000/multi/'

# this will be unique to each barrel.
BARREL_ID = 4

# able to toggle camera on/off
CAMERA = False
CAMERA_RES = (1640,1232)

# Measurement interval (in seconds)
MEASUREMENT_INT = 5400  # 1.5 hrs

# location where picture is writen before upload
PHOTO_LOC = 'most_recent_pic.jpg'

# location where log file will be written.
LOG_FILENAME = 'logs/growberry.log'
# the level at which to record logs:
LOG_LVL = logging.INFO
# logging format
LOG_FORMAT = "[%(levelname)s] %(name)s %(asctime)s %(message)s"


# CharacterLCD
LCD_PINS = False  # Make False if no LCD

# Uncomment the following block, and fill with the correct pin numbers

# LCD_PINS = { # Keys must all be here and unchanged.
#     'lcd_rs':27,
#     'lcd_en':22,
#     'lcd_d4':25,
#     'lcd_d5':24,
#     'lcd_d6':23,
#     'lcd_d7':18,
#     'lcd_backlight':4,
#     'lcd_columns':16,
#     'lcd_rows':2
#     }

