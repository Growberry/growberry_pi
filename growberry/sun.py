import datetime
from one_wire_temp import w1therm
from threading import Thread
from time import sleep
import logging

logger = logging.getLogger(__name__)

class Sun:
    """the sun class handles all tasks related to turning the lights on and off"""

    def __init__(self,lights,settings,maxtemp):
        self.settings = settings  # this is a Settings class
        self.lights = lights  # Relay class
        self.maxtemp = maxtemp
        self.heatsinksensor = w1therm()
        self.sinktemps = []
        # start monitoring heatsinks
        # t1 = Thread(target=self.safetyvalve, args=(self.lights,self.maxtemp))
        # t1.daemon = True
        # t1.start()
        logger.info('Let there be light!')


    def safetyvalve(self, lights, maxtemp):
        """Monitor the temp of the heatsinks.  If any of them exceed 55*C, power lights off. maxtemp = maxtemp"""
        logger.info('Heatsink safety monitor activated. Lights will be powered down if temps exceed {} C.'.format(maxtemp))
        while self:
            temps = self.heatsinksensor.gettemps()
            for temp in temps:  # temps is a dict: {'28-031655df8bff': 18.625, }
                tempfloat = float(temps[temp])
                self.sinktemps.append(tempfloat)
                # check if heatsinks are hotter than 50, if so, turn the lights off!
                if tempfloat > maxtemp:
                    lights.off()
                    # somehow notify the user.. email maybe?
                    logger.warning('ALERT: heatsink temp exceeded set value(%s).' % str(maxtemp))
                    logger.debug('current temps: %s. Temp that caused the problem: %s' % (','.join([str(x) for x in temps]), str(max(temps))))
            sleep(10)


    # def lightcontrol(self):
    #     """see if the lights should be on/off, and make them that way"""
    #     while self:
    #         sunrise = datetime.datetime.combine(datetime.date.today(), self.settings.sunrise)
    #         sunset = sunrise + self.settings.daylength
    #         if sunrise <= datetime.datetime.now() <= sunset:
    #             self.lights.on()
    #             logger.debug(' lights ON.  It is after sunrise (%s) and before sunset (%s).'%(sunrise,sunset))
    #         else:
    #             self.lights.off()
    #             logger.debug('lights OFF.  It is after sunset (%s).' % sunset)
    #         sleep(60)

    def lightcontrol(self):
        """
        determines if artificial lights should be on, or off.
        :param rise: datetime.time(h,m,s)
        :param length: integer number of hours
        :return: lights activate or deactivate.
        """
        while self:
            rise = self.settings.sunrise
            sunrise = datetime.datetime.combine(datetime.date.today(), rise)
            sunset = sunrise + self.settings.daylength
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


