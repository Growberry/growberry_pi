
from config import DHT22, RELAYS, SETTINGS_JSON, SETTINGS_URL, BARREL_ID, CAMERA, MAXTEMP,MEASUREMENT_INT
import RPi.GPIO as GPIO
from threading import Thread

from settings import Settings
from sun import Sun
if DHT22:  # if there are no sensors in config, don't need to import Adafruit (can cause trouble)
    import Adafruit_DHT
    from pins import Sensor
if RELAYS: # if no Relays configured, don't need Relay module
    from pins import Relay
if CAMERA:
    from picamera import PiCamera
from one_wire_temp import w1therm
from time import sleep


#set up all variables as None
camera = None
#sensors
in_sense = None
ext_sense = None
#relays
lights = None
fans = None
#settings
settings = None



"""import all the configured DH22 sensors, and set them up with names"""


for dht22_sensor in DHT22:
    # do I need to GPIO.setup() for DH22???
    if dht22_sensor[1] == 'internal':
        in_sense = Sensor(dht22_sensor[0], Adafruit_DHT.DHT22, dht22_sensor[1])
    elif dht22_sensor[1] == 'external':
        ext_sense = Sensor(dht22_sensor[0], Adafruit_DHT.DHT22, dht22_sensor[1])


"""import all the relays, and give them names"""

for relay in RELAYS:
    print type(relay)
    print relay
    GPIO.setup(relay[0], GPIO.OUT, initial=1)
    if relay[1] == 'lights':
        lights = Relay(relay[0],relay[1])
    elif relay[1] == 'fans':
        fans = Relay(relay[0], relay[1])

"""set up the Settings object that will handle all the settings"""

settings = Settings(SETTINGS_URL,SETTINGS_JSON,BARREL_ID)
settings.update()


"""set up camera"""
if CAMERA:
    camera = PiCamera()


"""set up 1wire temp for heatsinks"""
# heatsinktemps = w1therm()
# while True:
#     temps = heatsinktemps.gettemps()
#     for temp in temps:
#         #check if heatsinks are hotter than 50, if so, turn the lights off!
#         if temp > 50:
#             lights.off()
#             #somehow notify the user.. email maybe?
#     sleep(10)

sun = Sun(lights,settings,MAXTEMP)

try:
    while True:
        settings.update()
        sun.lightcontrol()
        # sunstatus = sun.status
        insense_report = in_sense.read
        data = [insense_report['timestamp'],insense_report['temp'],insense_report['humidity'],sun.sinktemps]
        sun.sinktemps = []
        print data
        sleep(MEASUREMENT_INT)
except(KeyboardInterrupt):
    print "growberry canceled manually."

finally:
    GPIO.cleanup()
    print "Pins are cleaned up, threads are killed.  Goodbye."


"""
{'lights': 1, 'heatsinktemps': {'28-031655df8bff': 21.0, 'timestamp': datetime.datetime(2016, 11, 13, 7, 1, 51, 598183)}}
{'timestamp': datetime.datetime(2016, 11, 13, 7, 1, 52, 124097), 'temp': 19.4, 'humidity': 79.3}
heatsink temp =  {'28-031655df8bff': 21.0, 'timestamp': datetime.datetime(2016, 11, 13, 7, 1, 52, 948184)}

"""