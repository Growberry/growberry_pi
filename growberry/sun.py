import datetime
from one_wire_temp import w1therm
from threading import Thread
from time import sleep

class Sun:
    """the sun class handles all tasks related to turning the lights on and off"""
    heatsinktemps = w1therm()
    def safetyvalve(self,lights,maxtemp):
        """monitor the temp of the heatsinks.  If any of them exceed 55*C"""
        while True:
            temps = self.heatsinktemps.gettemps()
            for temp in temps:
                # check if heatsinks are hotter than 50, if so, turn the lights off!
                if temp > maxtemp:
                    lights.off()
                    # somehow notify the user.. email maybe?
                    # also should log these alerts, not just print
                    print 'ALERT: heatsink temp exceeded set value(%s).' %str(maxtemp)
                    print 'current temps: ', temps
            sleep(10)


    def __init__(self,lights,settings):
        self.settings = settings # this is a Settings class
        self.lights = lights # Relay class

        # start monitoring heatsinks
        t1 = Thread(target = self.safetyvalve, kwargs = {'lights' = self.lights,'maxtemp' = 20})
        t1.start()

    def lightcontrol(self):
        # see if the lights should be on/off, and make them that way
        sunrise = datetime.datetime.combine(datetime.date.today(), self.settings.sunrise)
        sunset = sunrise + self.settings.daylength
        # testing print statement:
        print "rise: ", sunrise
        print "set", sunset
        print datetime.datetime.utcnow()
        if sunrise <= datetime.datetime.utcnow() <= sunset:
            self.lights.on()
            print "turning lights on...\n"
        else:
            self.lights.off()
            print "turning lights off...\n"



        # monitor heatsink temps, shut off when too hot

        # return lenth of time lights have been on
    @property
    def status(self):
        lightstatus = {'lights':self.lights.state,'heatsinktemps':self.heatsinktemps.gettemps()}
        # if self.lights.state:
        #     lightstatus['lights'] = True
        return lightstatus


