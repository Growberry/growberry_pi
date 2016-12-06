import os

basedir = os.path.abspath(os.path.dirname(__file__))

# A list containing all DH22 temp/humidity sensors
# if you add others, you need to set them up in __init__.py
DHT22 = [ #(pin number, 'name')
    (17, 'internal'),
#    (22,'external')
]

# a list containing all relays.  The names must be 'lights' and 'fans'
RELAYS = [ # (pin number, 'name')
    (6, 'lights')
    # ,(13, 'fans')
]

SETTINGS_URL = 'http://192.168.0.42:8000/get_settings/'
#SETTINGS_URL = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/get_settings/'

SETTINGS_JSON = os.path.join(basedir,'settings.json')

# data posting API
#DATAPOST_URL = 'http://ec2-54-244-205-179.us-west-2.compute.amazonaws.com/reading/'
DATAPOST_URL = 'http://192.168.0.42:8000/multi/'

# this will be unique to each barrel.
BARREL_ID = 4

# able to toggle camera on/off
CAMERA = False

# Maximum temp for heatsinks before safetycheck shuts the lights off
MAXTEMP = 30

# Measurement interval (in seconds)
MEASUREMENT_INT = 1800

# a test file to log to while testing
TEST_OUT = 'testout.txt'

# location where picture is writen before upload
PHOTO_LOC = 'testpic123.jpg'
