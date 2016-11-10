import datetime

class Sun:

    """the sun class handles all tasks related to turning the lights on and off"""
    def __init__(self,lights,settings):
        self.settings = settings # this is a Settings class
        self.lights = lights # Relay class
        # start monitoring heatsinks:
        # heatsinktemps = w1therm()
        # while True:
        #     temps = heatsinktemps.gettemps()
        #     for temp in temps:
        #         # check if heatsinks are hotter than 50, if so, turn the lights off!
        #         if temp > 50:
        #             lights.off()
        #             # somehow notify the user.. email maybe?
        #     sleep(10)
    def lightcontrol(self):
        sunrise = datetime.datetime.combine(datetime.date.today(), self.settings.sunrise)
        sunset = sunrise + self.settings.daylength

        if sunrise <= datetime.datetime.now() <= sunset:
            self.lights.on()
        else:
            self.lights.off()


        # see if the lights should be on/off, and make them that way

        # monitor heatsink temps, shut off when too hot

        # return lenth of time lights have been on
    @property
    def status(self):
        lightstatus = {'lights':False}

        if self.lights.state:
            lightstatus['lights'] = True
        return lightstatus


