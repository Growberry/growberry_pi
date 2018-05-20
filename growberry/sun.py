import datetime
import sys
import RPi.GPIO as GPIO
from one_wire_temp import w1therm
from time import sleep
import logging

GPIO.setmode(GPIO.BCM)  # for using the names of the pins
GPIO.setwarnings(True)  # set to false if the warnings bother you, helps troubleshooting

logger = logging.getLogger(__name__)

class Sun:
    """
    the sun class handles all tasks related to turning the lights on and off
    Will need two different cases of light control:  Binary and dimmable
    Will need a toggle for safety valve
    need to uncouple this from the settings class.  (done?)
    """

    def __init__(self, pins):
        self.powerpin = int(pins[0])  # this is the GPIO pin number (will depend on GPIO config)
        GPIO.setup(int(self.powerpin), GPIO.OUT, initial=1)
        self.mode = 'binary'
        if len(pins) == 2:
            self.dimpin = pins[1]
            self.mode = 'PWM'
            GPIO.setup(self.dimpin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.dimpin, 25000)  # need to pick a frequency that doesn't flicker the lights.
            self.pwm.start(0)
            self.brighness = 0
        logger.info('Let there be light!')
        self.heatsinksensor = w1therm()  # the w1therm class has methods to return all 1-wire sensor data in a dict.
        self.sinktemps = []

    @property
    def state(self):
        """ 0 is on, 1 is off """
        self._state = GPIO.input(self.powerpin)
        return self._state

    def sunup(self):
        """switches GPIO pin to LOW/0 - in open state relays, this turns the relay ON. (does nothing if relay already on (0))"""
        if self.state:
            GPIO.output(self.powerpin, GPIO.LOW)
            logger.info('Sun: ON')

    def sundown(self):
        """ switches GPIO pin to HIGH/1 - in open state relays, this turns the relay OFF.(does nothing if relay already off (1))"""
        if not self.state:
            GPIO.output(self.powerpin, GPIO.HIGH)
            logger.info('Sun: OFF')


    def safetyvalve(self, maxtemp):
        """
        Monitor the temp of the heatsinks.  If any of them exceed 55*C, power lights off. maxtemp = maxtemp
        using this function requires the use of 1-wire temp sensors mounted to the heatsinks
        This function also adds all the sensor data to the self.sinktemps list.  This list gets emptied in the get_data()
        """
        # read all heatsink sensors, make sure there is one
        logger.info('Heatsink safety monitor activated. Lights will be powered down if temps exceed {} C.'.format(maxtemp))
        while self:
            # self.sinktemps = w1therm().gettemps()  # temps is a dict: {'28-031655df8bff': 18.625, }
            for sensor_id, temp in self.heatsinksensor.gettemps().items():
                self.sinktemps.append(float(temp))
                if float(temp) > maxtemp:  # check if any sensor is hotter than the maxtemp
                    self.sundown()
                    logger.warning('ALERT: heatsink sensor {} reported a temp of {}, which exeeds the set max: {}'.format(sensor_id, temp, maxtemp))
            sleep(10)


    def lightcontrol(self, light_intervals):
        """
        determines if artificial lights should be on, or off.
        light_intervals is a list of tuples, consisting of (rise, daylength)
            :param rise: datetime.time(h,m,s)
            :param length: float or int number of hours
        :return: returns nothing. This actually turns lights on or off.
        eventually this will take any number of rises and lengths.  Perhaps in tuples
        """
        while self:
            decider = []
            for interval in light_intervals:  # interval should be a tuple of length 2.
                if isinstance(interval[0], datetime.time):
                    sunrise = datetime.datetime.combine(datetime.date.today(), interval[0])  #The day changes, but the time doesnt
                elif isinstance(interval[0], str) and len(interval[0]) == 4:
                    risetime = datetime.datetime.strptime(interval[0], '%H%M').time()
                    sunrise = datetime.datetime.combine(datetime.date.today(), risetime)
                else:
                    logger.error(
                        'The entered sunrise ({}) is not of datetime.time, or 4-digit string.\nIt appears to be of type: {}'.format(interval[0], type(interval[0])))
                    break
                if isinstance(interval[1], datetime.timedelta):
                    daylength = interval[1]
                elif isinstance(interval[1], int) or isinstance(interval[1], float):
                    daylength = datetime.timedelta(hours=interval[1])
                else:
                    logger.error('The entered daylength ({}) is not of datetime.timedelta, or int/float.\nIt appears to be of type: {}'.format(interval[1], type(interval[1])))
                    break
                sunset = sunrise + daylength

                now = datetime.datetime.now()
                tomorrow = now.date() + datetime.timedelta(hours=24)
                midnight = datetime.datetime.combine(tomorrow, datetime.time(0, 0, 0))
                if sunrise <= midnight <= sunset:
                    logger.debug('day spans midnight')
                    if sunset.time() <= now.time() <= sunrise.time():
                        decider.append('off')  # The current time is NOT within this lighting interval
                        logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights OFF.'.format(sunrise, sunset,
                                                                                      datetime.datetime.now().time()))
                    else:
                        decider.append('on')  # The current time is within this lighting interval
                        logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights ON.'.format(sunrise, sunrise,
                                                                                     datetime.datetime.now().time()))
                else:
                    if sunrise.time() <= now.time() <= sunset.time():
                        decider.append('on')  # The current time is within this lighting interval
                        logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights ON.'.format(sunrise, sunset,
                                                                                               datetime.datetime.now()))
                    else:
                        decider.append('off')  # The current time is NOT within this lighting interval
                        logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights OFF.'.format(sunrise, sunset,
                                                                                       datetime.datetime.now()))

                # if the decider list has any 'on' values, the current time falls within one of the intervals, so the lights should be on!
                if 'on' in decider:
                    self.sunup()
                else:
                    self.sundown()

                sleep(60)

                        # return lenth of time lights have been on
    @property
    def status(self):
        lightstatus = {'lights':self.state,'sinktemps':self.heatsinksensor.gettemps()}
        # if self.lights.state:
        #     lightstatus['lights'] = True
        return lightstatus


# Manual mode:

if __name__ == '__main__':
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setLevel(logging.DEBUG)
    logger.addHandler(out_hdlr)

<<<<<<< HEAD
    power = raw_input("Which GPIO pin powers the lights?\n>>>")
    pwm = raw_input("Which pin controls the brightness (this doesn't do anything yet)?\n>>>")
    sun = Sun(int(power),int(pwm))
    print('lights are currently: {}'.format(sun.state))
    sun.sunup()
    sleep(3)
    print('lights are currently: {}'.format(sun.state))
=======
    power = input("Which GPIO pin powers the lights?\n>>>")
    pwm = input("Which pin controls the brightness (this doesn't do anything yet)?\n>>>")
    sun = Sun(int(power), int(pwm))
    logger.debug('lights are currently: {}'.format(sun.state))
    sun.sunup()
    sleep(3)
    logger.debug('lights are currently: {}'.format(sun.state))
>>>>>>> 9e4498d7f516c5548d1b98ecd321807eeb2f64ec
    sun.sundown()
    logger.debug('lights are currently: {}'.format(sun.state))

    while True:
<<<<<<< HEAD
        user_sunrise = raw_input("what time does the sun come up (HHMM)?\n>>>")
        user_daylenth = raw_input("how long is the sun up for (in hours)?\n>>>")
        user_interval = [(user_sunrise, user_daylenth)]
        print(user_interval)
        sun.lightcontrol(user_interval)
        print('lights are currently: {}'.format(sun.state))
    sun.sundown()
    GPIO.cleanup()
    print('Sun has set, GPIO pins have been cleaned up. Goodbye.')
=======
        user_sunrise = str(input("what time does the sun come up (HHMM)?\n>>>"))
        user_daylenth = float(input("how long is the sun up for (in hours)?\n>>>"))
        user_interval = [(user_sunrise, user_daylenth)]
        logger.debug('Entered interval: {}'.format(user_interval))
        print('length of interval: {}'.format(len(user_interval)))
        print('type of interval: {}'.format(type(user_interval)))
        sun.lightcontrol(user_interval)
        logger.debug('lights are currently: {}'.format(sun.state))
    sun.sundown()
    GPIO.cleanup()
    logger.debug('Sun has set, GPIO pins have been cleaned up. Goodbye.')


    """
Exception in thread Thread-15:
Traceback (most recent call last):
  File "/usr/lib/python2.7/threading.py", line 810, in __bootstrap_inner
    self.run()
  File "/usr/lib/python2.7/threading.py", line 763, in run
    self.__target(*self.__args, **self.__kwargs)
  File "growberry/sun.py", line 85, in lightcontrol
    if isinstance(interval[0], datetime.time):
TypeError: 'datetime.time' object has no attribute '__getitem__'
"""
>>>>>>> 9e4498d7f516c5548d1b98ecd321807eeb2f64ec
