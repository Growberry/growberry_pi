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
        self.mt = maxtemp
        self.heatsinksensor = w1therm()
        self.sinktemps = []
        # start monitoring heatsinks
        t1 = Thread(target=self.safetyvalve, args=(self.lights,self.mt))
        t1.daemon = True
        t1.start()
        logger.info('Let there be light!')


    def safetyvalve(self, lights, mt):
        """Monitor the temp of the heatsinks.  If any of them exceed 55*C, power lights off. mt = maxtemp"""
        while self:
            temps = self.heatsinksensor.gettemps()
            for temp in temps:  # temps is a dict: {'28-031655df8bff': 18.625, 'timestamp': datetime.datetime(2016, 11, 11, 22, 47, 35, 344949)}
                if temp == 'timestamp':
                    continue
                else:
                    tempfloat = float(temps[temp])
                    self.sinktemps.append(tempfloat)
                    # check if heatsinks are hotter than 50, if so, turn the lights off!
                    if tempfloat > mt:
                        lights.off()
                        # somehow notify the user.. email maybe?
                        logger.warning('ALERT: heatsink temp exceeded set value(%s).' % str(mt))
                        logger.warning('current temps: ', temps, "Temp that caused the problem: ", temp, str(temps[temp]))
            sleep(10)


    def lightcontrol(self):
        """see if the lights should be on/off, and make them that way"""
        while self:
            sunrise = datetime.datetime.combine(datetime.date.today(), self.settings.sunrise)
            sunset = sunrise + self.settings.daylength
            if sunrise <= datetime.datetime.now() <= sunset:
                self.lights.on()
                logger.debug('it is after sunrise (%s) and before sunset (%s), lights ON.'%(sunrise,sunset))
            else:
                self.lights.off()
                logger.debug('it is after sunset (%s), lights OFF.' % sunset)
        sleep(60)

        # return lenth of time lights have been on
    @property
    def status(self):
        lightstatus = {'lights':self.lights.state,'heatsinksensor':self.heatsinksensor.gettemps()}
        # if self.lights.state:
        #     lightstatus['lights'] = True
        return lightstatus


