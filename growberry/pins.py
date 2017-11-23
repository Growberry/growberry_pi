import time
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_DHT
import datetime
import logging

logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)  # for using the names of the pins
GPIO.setwarnings(True)  # set to false if the warnings bother you, helps troubleshooting

class Relay:
    """
    Turns GPIO pins from LOW(on) to HIGH(off) and back again.  Remember: relays are inverted.
    3.3v turns the relay off.

    this class pretty much works for any device connected to a single GPIO pin
    as instances of Relays are created, their names are added as keys in the Relay.dictionary
    """
    dictionary = {}  # a dictionary will all created Pin instances' names as keys

    # state = None
    def __init__(self, pin, name):
        self.pin = int(pin)  # this is the GPIO pin number (will depend on GPIO config)
        self.name = name
        GPIO.setup(pin, GPIO.OUT, initial=1)
        Relay.dictionary[name] = self  # auto adds every instance of Relay to the dictionary

    @property
    def state(self):
        """ 0 is on, 1 is off """
        self._state = GPIO.input(self.pin)
        return self._state

    def on(self):
        """switches GPIO pin to LOW/0 - in open state relays, this turns the relay ON. (does nothing if relay already on (0))"""
        if self.state:
            GPIO.output(self.pin, GPIO.LOW)
            logger.info('{} turned ON'.format(self.name))

    def off(self):
        """ switches GPIO pin to HIGH/1 - in open state relays, this turns the relay OFF.(does nothing if relay already off (1))"""
        if not self.state:
            GPIO.output(self.pin, GPIO.HIGH)
            logger.info('{} turned OFF\n'.format(self.name))

    def blink(self, *args):
        """this should not be used for actual relays, just LEDs"""
        # print (len(args))          #troubleshooting print statement
        # print args                 # another
        try:
            repeat = int(args[0])   # if arguments are included, use the first one to mean number of blinks
        except:
            repeat = 1              # default is 1 blink
        try:
            speed = (float(args[1])) / 2    # second argument is the speed of blinks
        except:
            speed = .5              # default is .5 seconds
        # print repeat               #troubleshooting print statement
        # print speed                # another
        # color: uncomment below for color export to terminal.
        # print("%s Relay is" % self.name + bcolors.BOLD + bcolors.PURPLE + " blinking." + bcolors.END)
        while repeat > 0:
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(speed)
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(speed)
            repeat -= 1



class Sensor:
    array = []
    def __init__(self, pin, sens_type, name):
        self.sens_type = sens_type
        self.pin = int(pin)  # this is the GPIO pin number (will depend on GPIO config)$
        self.name = name  #
        Sensor.array.append(self)

    @property
    def read(self):
        """
        Sometimes the sensor will return "None"
        This might happen if the CPU is under a lot of load and the sensor
        this property method attempts to read the dht22 3 times before logging an error
        will return 'NA' for failed values.
        """
        attempts = 0
        while attempts < 3:
            try:
                humidity, temp = Adafruit_DHT.read(self.sens_type, self.pin)
                if humidity and temp:
                    return {"%s" % self.name: {"temp": round(float(temp), 1), "humidity": round(float(humidity), 1),
                                               "timestamp": datetime.datetime.utcnow().isoformat()}}
                logger.debug('%s DHT22 sensor read failed! Attempts remaining: {}'.format(self.name, 2-attempts))
                raise TypeError('could not read sensor.')
            except TypeError:
                attempts += 1
                time.sleep(2)
        logger.error('{}-DHT22 sensor could not be reached after 3 attempts.  Make sure sensor is connected to GPIO {}'.format(self.name,str(self.pin)))
        return {"%s" % self.name: {"temp": 'NA', "humidity": 'NA',"timestamp": datetime.datetime.utcnow().isoformat()}}

        #print 'Temperature: {0:0.1f} C'.format(temp)       #prints Temp formated
        #print 'Humidity:    {0:0.1f} %'.format(humidity)   #prints Humidity formatted


if __name__=="__main__":
    print('Entering manual mode:  Currently only supporting DHT22 sensors.')
    sleep(1)
    # put in a handler to print errors to the standard output
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setLevel(logging.DEBUG)
    logger.addHandler(out_hdlr)
    sensor_pins = None

    # take any number of DHT22 sensors, and the pins they are on.
    try:
        sensor_number = int(input('how many DHT22 sensors are connected?\n>>>'))
        sensor_pins = [int(input('which pin is connected to your DHT22?\n>>>')) for x in range(sensor_number)]

    except ValueError:
        logger.error('all values entered must be integers!')

    manual_sensors = None
    for sensor in sensor_pins:  # create a list containing all the sensor objects
        manual_sensors.append(Sensor(sensor, Adafruit_DHT.DHT22, 'DHT22 on pin:{}'.format(sensor)))

    while True:
        sensor_data = {}
        for s in manual_sensors:
            sensor_data.update(s.read)

        print(sensor_data)