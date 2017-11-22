import datetime
from one_wire_temp import w1therm
from threading import Thread
from time import sleep
import logging

logger = logging.getLogger(__name__)

class Sun:
    """
    the sun class handles all tasks related to turning the lights on and off
    Will need two different cases of light control:  Binary and dimmable
    Will need a toggle for safety valve
    need to uncouple this from the settings class.  (done?)
    """

    def __init__(self, powerpin, dim_pin=False):
        self.powerpin = int(powerpin)  # this is the GPIO pin number (will depend on GPIO config)
        GPIO.setup(powerpin, GPIO.OUT, initial=1)
        self.mode = 'binary'
        if dim_pin:
            self.dimpin = dim_pin
            self.mode = 'PWM'
            GPIO.setup(dim_pin, GPIO.OUT)
            self.pwm = GPIO.PWM(dim_pin, 25000)  # need to pick a frequency that doesn't flicker the lights.
            self.pwm.start(0)
            self.brighness = 0
        logger.info('Let there be light!')




    @property
    def state(self):
        """ 0 is on, 1 is off """
        self._state = GPIO.input(self.pin)
        return self._state

    def on(self):
        """switches GPIO pin to LOW/0 - in open state relays, this turns the relay ON. (does nothing if relay already on (0))"""
        if self.state:
            GPIO.output(self.powerpin, GPIO.LOW)
            logger.info('Sun: ON')

    def off(self):
        """ switches GPIO pin to HIGH/1 - in open state relays, this turns the relay OFF.(does nothing if relay already off (1))"""
        if not self.state:
            GPIO.output(self.powerpin, GPIO.HIGH)
            logger.info('Sun: OFF')





    def __init__(self,light_relay_pin, lights,sunrise, daylength, maxtemp):




    def safetyvalve(self, maxtemp):
        """Monitor the temp of the heatsinks.  If any of them exceed 55*C, power lights off. maxtemp = maxtemp"""
        # read all heatsink sensors, make sure there is one
        logger.info('Heatsink safety monitor activated. Lights will be powered down if temps exceed {} C.'.format(maxtemp))
        while self:
            self.heatsinksensor = w1therm()
            self.sinktemps = []
            temps = self.heatsinksensor.gettemps()

            sinktemps = w1therm().gettemps()  # temps is a dict: {'28-031655df8bff': 18.625, }
            for sensor_id, temp in sinktemps.items():
                if float(temp) > maxtemp:
                    self.off()
                    logger.warning('ALERT: heatsink sensor {} reported a temp of {}, which exeeds the set max: {}'.format(sensor_id, temp, maxtemp))
            # for temp in temps:  # temps is a dict: {'28-031655df8bff': 18.625, }
            #     tempfloat = float(temps[temp])
            #     self.sinktemps.append(tempfloat)
            #     # check if heatsinks are hotter than 50, if so, turn the lights off!
            #     if tempfloat > maxtemp:
            #         self.off()
            #         # somehow notify the user.. email maybe?
            #         logger.warning('ALERT: heatsink temp exceeded set value(%s).' % str(maxtemp))
            #         logger.debug('current temps: %s. Temp that caused the problem: %s' % (','.join([str(x) for x in temps]), str(max(temps))))
            sleep(10)


    def lightcontrol(rise, daylength):
        """
        determines if artificial lights should be on, or off.
        :param rise: datetime.time(h,m,s)
        :param length: float number of hours
        :return: returns nothing. This actually turns lights on or off.
        """
        while self:
            sunrise = datetime.datetime.combine(datetime.date.today(), rise)
            daylen = datetime.timedelta(hours=float(daylength))  # convert the float to a timedelta for addition
            sunset = sunrise + daylen
            set = sunset.time()
            now = datetime.datetime.now()
            tomorrow = now.date() + datetime.timedelta(hours=24)
            midnight = datetime.datetime.combine(tomorrow, datetime.time(0, 0, 0))
            if sunrise <= midnight <= sunset:
                logger.debug('day spans midnight')
                if set <= now.time() <= rise:
                    self.lights.off()
                    logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights OFF.'.format(rise, set,
                                                                                  datetime.datetime.now().time()))
                else:
                    self.lights.on()
                    logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights ON.'.format(rise, set,
                                                                                 datetime.datetime.now().time()))
            else:
                if rise <= now.time() <= set:
                    self.lights.on()
                    logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights ON.'.format(sunrise, sunset,
                                                                                           datetime.datetime.now()))
                else:
                    self.lights.off()
                    logger.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights OFF.'.format(sunrise, sunset,
                                                                                            datetime.datetime.now()))
            sleep(60)

                        # return lenth of time lights have been on
    @property
    def status(self):
        lightstatus = {'lights':self.lights.state,'heatsinksensor':self.heatsinksensor.gettemps()}
        # if self.lights.state:
        #     lightstatus['lights'] = True
        return lightstatus


