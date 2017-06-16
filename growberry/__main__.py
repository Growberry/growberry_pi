
from time import sleep
import datetime
from threading import Thread
import json
import requests
import logging
import logging.handlers

import RPi.GPIO as GPIO
from picamera import PiCamera

from config import DHT22, RELAYS, SETTINGS_JSON, SETTINGS_URL, BARREL_ID, CAMERA, CAMERA_RES, MAXTEMP, MEASUREMENT_INT,\
    DATAPOST_URL, PHOTO_LOC, LOG_FILENAME, LOG_LVL, LOG_FORMAT, FANS, LCD_TRUE, LCD_PINS

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
if LCD_TRUE:
    import Adafruit_CharLCD as LCD


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
logger.info("DHT22 sensors configured: {}".format(str_sensor))


"""import all the relays, and give them names"""
for relay in RELAYS:
    GPIO.setup(relay[0], GPIO.OUT, initial=1)
    if relay[1] == 'lights':
        lights = Relay(relay[0],relay[1])
    elif relay[1] == 'fans':
        # wind = Wind(13, 18)
        fans = Relay(relay[0], relay[1])
str_relays = ','.join([str(x) for x in Relay.dictionary.items()])
logger.info('Relays configured: {}'.format(str_relays))


"""set up the Settings object that will handle all the settings"""
settings = Settings(SETTINGS_URL,SETTINGS_JSON,BARREL_ID)
settings.update()



"""set up camera"""
if CAMERA:
    camera = PiCamera()
    camera.resolution = CAMERA_RES
    logger.info('camera configured.')

"""setting up lights"""
sun = Sun(lights,settings,MAXTEMP)

"""setting up fans"""
# wind = Wind(13,18)
wind = Wind(FANS[0],FANS[1])

"""setting up LCD display"""
if LCD_TRUE:
    # Initialize the LCD using the pins from LCD_PINS.
    lcd = LCD.Adafruit_CharLCD(
        LCD_PINS['lcd_rs'], LCD_PINS['lcd_en'], LCD_PINS['lcd_d4'],
        LCD_PINS['lcd_d5'], LCD_PINS['lcd_d6'], LCD_PINS['lcd_d7'],
        LCD_PINS['lcd_columns'], LCD_PINS['lcd_rows'], LCD_PINS['lcd_backlight'])
LCD_TOP = 'Nothing to'
LCD_BOT = 'display yet.'


def fancontrol_binary(settings, i_temp, i_humidity, o_temp, sinktemp, lightstate):
    """used for simple on/off fans"""
    fanspeed = 0
    if i_humidity > settings.sethumid:
        fanspeed = 1
    if i_temp > settings.settemp:
        fanspeed = 1
    return fanspeed

def fancontrol(settings, i_temp, i_humidity, o_temp, sinktemp, lightstate):
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
    if i_humidity > settings.sethumid:
        beta = 5
    io_delta = o_temp - i_temp  #
    delta_t = settings.settemp - i_temp  # pos values means we want the temp to go up, neg = want temps to go down.
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
    Literally only deterimines what speed the fan should be.  Pass in the lights, fans, and all inputs.
    reads the inputs, and passes them to the correct fanspeed function (binary or PWM)
    """
    global LCD_TOP
    global LCD_BOT
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
                internal_humidity = float(in_sensor.read[in_sensor.name]['humidity'])
                external_temp = float(out_sensor.read[out_sensor.name]['temp'])
                LCD_BOT = 'online:{}'.format(settings['online'])
            except ValueError:
                logger.warning('one of the sensors could not be read, defaults used.')
                LCD_BOT = 'DEFAULTS USED'
            except:
                logger.exception("unknown error, defaults used.")
            fspeed = fancontrol(settings, internal_temp, internal_humidity, external_temp, heatsink_max, lightstatus)
            wind.speed(fspeed)
            if LCD_TRUE:
                lcd.message('{}\n{}'.format(LCD_TOP,LCD_BOT))
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
        logger.debug('Files for upload: {}'.format(files_json))
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
            logger.debug('the URL where the data is headed: {}'.format(url))
            data_capture(url)
            sleep(MEASUREMENT_INT)
    except:
        logger.exception('data_logger() failed. Data failed to be uploaded')


workers = {
    'lighting': Thread(target=sun.lightcontrol),
    'hvac': Thread(target=thermostat, args=(sun, wind, in_sense, ext_sense, settings)),
    'heatink_safety_monitor': Thread(target=sun.safetyvalve, args=(sun.lights,sun.maxtemp)),
    'settings_fetcher': Thread(target=settings_fetcher),
    'data_logger': Thread(target=data_logger)
}

for name in workers:
    workers[name].daemon = True
    workers[name].start()
    sleep(1)

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
    if LCD_TRUE:
        lcd.clear()
    GPIO.cleanup()
    logger.info("Pins are cleaned up, threads are killed.  Goodbye.")


