import datetime

class Sun:

    """the sun class handles all tasks related to turning the lights on and off"""
    def __init__(self,lights,settings):
        self.settings = settings # this is a Settings class
        self.lights = lights # Relay class
        # self._
    def lightcontrol(self):
        """send in the time to turn the lights on, and how long to keep them on for. Returns a light status"""
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
    def status():
        if self.lights.state:


