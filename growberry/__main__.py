
from config import DHT22, RELAYS, SETTINGS_JSON, SETTINGS_URL, BARREL_ID, CAMERA, MAXTEMP,MEASUREMENT_INT, TEST_OUT, DATAPOST_URL, PHOTO_LOC
import RPi.GPIO as GPIO
from threading import Thread
import json
import requests
from picamera import PiCamera
import logging



from settings import Settings
from sun import Sun
from wind import Wind
if DHT22:  # if there are no sensors in config, don't need to import Adafruit (can cause trouble)
    import Adafruit_DHT
    from pins import Sensor
if RELAYS: # if no Relays configured, don't need Relay module
    from pins import Relay
if CAMERA:
    from picamera import PiCamera
from one_wire_temp import w1therm
from time import sleep
import datetime


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

logger = logging.getLogger(__name__)
logging_format = "[%(levelname)s] %(name)s %(asctime)s %(message)s"
logging.basicConfig(filename='log_growberry.log',format=logging_format, level=logging.DEBUG)



"""import all the configured DH22 sensors, and set them up with names"""
for dht22_sensor in DHT22:
    if dht22_sensor[1] == 'internal':
        in_sense = Sensor(dht22_sensor[0], Adafruit_DHT.DHT22, dht22_sensor[1])
    elif dht22_sensor[1] == 'external':
        ext_sense = Sensor(dht22_sensor[0], Adafruit_DHT.DHT22, dht22_sensor[1])
str_sensor = ','.join([str(x) for x in Sensor.array])
logger.info("DHT22 sensors configured: %s" %str_sensor)


"""import all the relays, and give them names"""
for relay in RELAYS:
    GPIO.setup(relay[0], GPIO.OUT, initial=1)
    if relay[1] == 'lights':
        lights = Relay(relay[0],relay[1])
    elif relay[1] == 'fans':
        fans = Relay(relay[0], relay[1])
str_relays = ','.join([str(x) for x in Relay.dictionary.items()])
logger.info('Relays configured: %s' %str_relays)


"""set up the Settings object that will handle all the settings"""
settings = Settings(SETTINGS_URL,SETTINGS_JSON,BARREL_ID)
settings.update()



"""set up camera"""
if CAMERA:
    camera = PiCamera()
    logger.info('camera configured.')

# setting up lights
sun = Sun(lights,settings,MAXTEMP)
# lighting = Thread(target=sun.lightcontrol)
# lighting.daemon = True
# lighting.start()

# setting up fans
wind = Wind(13,18)
# hvac = Thread(target=thermostat, args=(lights, wind, in_sense))
# hvac.daemon = True
# hvac.start()

def thermostat(lights, wind, sensor):
    while True:
        night = lights.state  # when the lights.state is 1, the lights are off
        fanspeed = wind.tach
        # the max temp I'd expect is 50C, so if you divide by 50, and times 100, you get a percentage
        percentfan = round(((sensor.read[sensor.name]['temp']) / 50) * 100, ndigits=1)
        if not night:
            wind.speed(percentfan)
            logger.debug('fans ON and set to speed %s' %percentfan)
        else:
            wind.speed(0)
            logger.debug('fans OFF')
        sleep(60)

def data_capture(url):
    sensor_data = {}
    for sensor in Sensor.array:
        sensor_data.update(sensor.read)
    data = {
        'timestamp': datetime.datetime.utcnow().isoformat(),  # datetime
        'sinktemps': sun.sinktemps,  # list of float object
        'sensors': sensor_data,  # dict {'name':{'timestamp','temp','humidity'}}
        'lights': lights.state,  # bool
        'fanspeed': wind.tach,  # float
        'pic_dir': '/tmp/placeholder'  # replace this with an actual directory when pictures are working
            }
    sun.sinktemps = []
    logger.debug('sinktemp list reset.')

    files = {
        'metadata': ('metadata.json', json.dumps(data), 'application/json'),
            }

    if camera:
        camera.capture(PHOTO_LOC)
        files.update({'photo': (PHOTO_LOC, open(PHOTO_LOC, 'rb'), 'image/jpg')})
    files_json = ','.join(str(x) for x in files.keys()) 
    logger.debug('Files for upload: %s' % files_json)
    r = requests.post(url, files=files)
    logger.info(r.text)
    # return r

def settings_fetcher():
    while True:
        settings.update()
        sleep(MEASUREMENT_INT)

def data_logger():
    while True:
        url = DATAPOST_URL + str(BARREL_ID)
        logger.debug('the URL where the data is headed: %s' % url)
        data_capture(url)
        sleep(MEASUREMENT_INT)



workers = {
    'heatink_safety_monitor': Thread(target=sun.safetyvalve, args=(sun.lights,sun.maxtemp)),
    'lighting': Thread(target=sun.lightcontrol),
    'hvac': Thread(target=thermostat, args=(lights, wind, in_sense)),
    'settings_fetcher': Thread(target=settings_fetcher),
    'data_logger': Thread(target=data_logger)
}

for name in workers:
    workers[name].daemon = True
    workers[name].start()

try:
    while True:
        sleep(1)
        for name in workers:
            if not workers[name].is_alive():
                logger.warning('{} encountered an error! Restarting...'.format(name))
                if name == 'heatink_safety_monitor':
                    workers[name] = Thread(target=sun.safetyvalve, args=(sun.lights,sun.maxtemp))
                elif name == 'lighting':
                    workers[name] = Thread(target=sun.lightcontrol)
                elif name == 'hvac':
                    workers[name] = Thread(target=thermostat, args=(lights, wind, in_sense))
                elif name == 'settings_fetcher':
                    workers[name] = Thread(target=settings_fetcher)
                elif name == 'data_logger':
                    workers[name] = Thread(target=data_logger)

                workers[name].daemon = True
                workers[name].start()

except(KeyboardInterrupt):
    logger.warning('growberry canceled manually.')


finally:
    GPIO.cleanup()
    logger.info("Pins are cleaned up, threads are killed.  Goodbye.")



    # while True:
    #     settings.update()
    #     logger.debug('settings updated')
    #     # sun.lightcontrol()
    #     # print "lights updated"
    #
    #     url = DATAPOST_URL + str(BARREL_ID)
    #     logger.debug('the URL where the data is headed: %s' % url)
    #     data_capture(url)

    # data_json = json.dumps(data)
    # print data_json
    # r = requests.post(url, headers=headers, data=data_json)  # data
    # returned_headers = str(r.headers)
    # print 'returned: ', r, 'of type: ', type(r)
    # print '\nthe text of which is: ', r.text
    # # print data
    # sun.sinktemps = []
    # #str_sinks = '|'.join([str(x) for x in data['sinktemps']])
    # # FIX THIS SO IT CAN MAKE A STRING DYNAMICALLY, and print the HEADERS
    # data_str = '\t'.join([str(x) for x in [data['timestamp'],
    #                                        data['lights'],
    #                                        data['fanspeed'],
    #                                        sensor_data['internal']['temp'],
    # #                                       sensor_data['external']['temp'],
    #                                        sensor_data['internal']['humidity'],
    # #                                       sensor_data['external']['humidity'],
    # #                                       str_sinks,
    #                                        ]])
    # print data_str
    # data = [insense_report['timestamp'].isoformat(), lights.state, insense_report['temp'],insense_report['humidity'],sun.sinktemps]

    # print data
    # d = "%s\t%s\tlights:%s\t%s\t%s\n" % (str(data[0]), str(data[1]), str(data[2]), str(data[3]))


    # with open(TEST_OUT,'a') as outfile:
    #     outfile.write(data_str)
    #     outfile.write('\n')

    # sleep(MEASUREMENT_INT)