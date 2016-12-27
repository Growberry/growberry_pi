
from config import DHT22, RELAYS, SETTINGS_JSON, SETTINGS_URL, BARREL_ID, CAMERA, MAXTEMP,MEASUREMENT_INT,\
    TEST_OUT, DATAPOST_URL, PHOTO_LOC, LOG_FILENAME, LOG_LVL, LOG_FORMAT
import RPi.GPIO as GPIO
from threading import Thread
import json
import requests
from picamera import PiCamera
import logging
import logging.handlers


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

global_logger = logging.getLogger()
global_logger.setLevel(logging.DEBUG)

# logger = logging.getLogger(__name__)
# logging_format = "[%(levelname)s] %(name)s %(asctime)s %(message)s"
# logging.basicConfig(filename='log_growberry.log',format=logging_format, level=LOG_LVL)

# Set up a specific logger with our desired output level
logger = logging.getLogger(__name__)

# Add the log message handler to the logger
file_handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1 * 1024 * 1024, backupCount=2)
file_handler.setLevel(LOG_LVL)

# Add a formatter
formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)

global_logger.addHandler(file_handler)

# # Add another handler that will stream to output
# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.ERROR)
# logger.addHandler(stream_handler)


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


def fancontrol(set_temp, i_temp, i_humidity, o_temp, sinktemp, lightstate):
    """
    fan speed model:  fanspeed = alpha(lightstatus) + beta(heatsink_max) + gamma(internal_temp) + delta(internal_humidity)

    :alpha: +5 if lights ON
    :beta: +5 if humidity is over 85
    :gamma: delta(settemp - in_temp) * delta(out_temp - in_temp) / 10
    :epsilon: (sinktemp-30) * 6.34

    :return: speed at which to set the fan (0-100) in multiples of 5.
    """
    alpha = -5 * (lightstate - 1)
    beta = 0
    if i_humidity > 85:
        beta = 5
    io_delta = o_temp - i_temp  #
    delta_t = set_temp - i_temp  # pos values means we want the temp to go up, neg = want temps to go down.
    temp_coef = io_delta * delta_t  # will return positive values if both match
    gamma = 0
    if temp_coef > 0:
        gamma = temp_coef/10
    epsilon = max(0,(sinktemp - 30) * 6.34)

    omega = alpha + beta + gamma + epsilon
    logger.debug('omega = alpha + beta + gamma + epsilon\n{}(fanspeed) = {}(lights) + {}(humidity) + {}(temp_coef) + {}(heatsink)'.format(omega,alpha,beta,gamma,epsilon))
    fanspeed = min(100, int(round(omega/5)*5))
    return fanspeed



def thermostat(sun, wind, in_sensor, out_sensor, settings):
    """

    """
    try:
        while True:
            lightstatus = sun.lights.state
            heatsink_max = 45.0  # default
            try:
                heatsink_max = max(sun.heatsinksensor.gettemps().values())
            except:
                logger.exception("couldn't read heatsink sensor. Default 45.0 used.")
            internal_temp = 25.0  # default
            internal_humidity = 50.0  # default
            external_temp = 25.0  # default
            try:
                internal_temp = float(in_sensor.read[in_sensor.name]['temp'])
                internal_humidity = float(in_sensor.read[in_sensor.name]['humidty'])
                external_temp = float(out_sensor.read[out_sensor.name]['temp'])
            except ValueError:
                logger.warning('one of the sensors could not be read, defaults used.')
            except:
                logger.exception("unknown error, defaults used.")

            fspeed = fancontrol(settings.settemp, internal_temp, internal_humidity, external_temp, heatsink_max, lightstatus)
            wind.speed(fspeed)

            #
            # night = lights.state  # when the lights.state is 1, the lights are off
            # fanspeed = wind.tach
            # # the max temp I'd expect is 50C, so if you divide by 50, and times 100, you get a percentage
            # try:
            #     current_temp = sensor.read[sensor.name]['temp']
            #     percentfan = round((current_temp / 50) * 100, ndigits=1)
            # except TypeError:
            #     percentfan = 50
            #     logger.exception('{} could not be read, setting fans to default 50%'.format(sensor.name))
            # if not night:
            #     wind.speed(percentfan)
            #     logger.debug('fans ON and set to speed %s' %percentfan)
            # else:
            #     wind.speed(0)
            #     logger.debug('fans OFF')
            sleep(60)
    except:
        logger.exception('thermostat broke')

def data_capture(url):
    try:
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
        logger.debug('data has been read. sinktemp list reset.')

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

    except:
        logger.exception('data_capture() failed.  data has was not uploaded')

def settings_fetcher():
    try:
        while True:
            settings.update()
            sleep(MEASUREMENT_INT)
    except:
        logger.exception('settings_fetcher() failed. settings not updated.')

def data_logger():
    try:
        while True:
            url = DATAPOST_URL + str(BARREL_ID)
            logger.debug('the URL where the data is headed: %s' % url)
            data_capture(url)
            sleep(MEASUREMENT_INT)
    except:
        logger.exception('data_logger() failed. Data failed to be uploaded')


workers = {
    'heatink_safety_monitor': Thread(target=sun.safetyvalve, args=(sun.lights,sun.maxtemp)),
    'lighting': Thread(target=sun.lightcontrol),
    'hvac': Thread(target=thermostat, args=(sun, wind, in_sense, ext_sense, settings)),
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
                    workers[name] = Thread(target=thermostat, args=(sun, wind, in_sense, ext_sense, settings)) #sun, wind, in_sensor, out_sensor, settings
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