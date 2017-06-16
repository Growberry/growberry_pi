import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)  # for using the names of the pins
GPIO.setwarnings(True)  # set to false if the warnings bother you, helps troubleshooting

logger = logging.getLogger(__name__)

class Wind:
    """This will house all of functions used to control the fans"""
    # def __init__(self, powerpin, speedpin, speed = 0):
    #     self.powerpin = powerpin
    #     GPIO.setup(powerpin, GPIO.OUT, initial=1)
    #     GPIO.setup(speedpin, GPIO.OUT)
    #     self.pwm = GPIO.PWM(speedpin, 25000) # 25 Kilohertz is inaudible to human ears
    #     self.pwm.start(speed)
    #     self.tach = speed
    #     logger.info('fans initiated.  Power on pin {}, speed control PWM on pin {}'.format(self.powerpin,self.pwm))

    def __init__(self, *args):
        if len(args) == 1:
            self.fantype = 'Binary'
        elif len(args) == 2:
            self.speedpin = args[1]
            GPIO.setup(self.speedpin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.speedpin, 25000) # 25 Kilohertz is inaudible to human ears
            self.pwm.start(0)
            self.tach = 0
            self.fantype = 'PWM'
        else:
            logger.error('Wind class accepts only 1-2 arguments')
            raise ValueError("wrong number of arguments")
        self.powerpin = args[0]
        GPIO.setup(self.powerpin, GPIO.OUT, initial=1)
        logger.info('Wind instance configured using {} fans.  Power on pin {}'.format(self.fantype, self.powerpin))


    # def fancontrol_binary(self, settings, i_temp, i_humidity, o_temp, sinktemp, lightstate):
    #     """used for simple on/off fans"""
    #     fanspeed = 0
    #     if i_humidity > settings.sethumid:
    #         fanspeed = 1
    #     if i_temp > settings.settemp:
    #         fanspeed = 1
    #     return fanspeed

    def fancontrol(self, settings, i_temp, i_humidity, o_temp, sinktemp, lightstate):
        """
        Binary fan speed model uses temp/humidity thresholds found in settings
        PWM fan speed model:  fanspeed = alpha(lightstatus) + beta(heatsink_max) + gamma(internal_temp) + delta(internal_humidity)

        :alpha: +5 if lights ON
        :beta: +5 if humidity is over 85
        :gamma: delta(settemp - in_temp) * delta(out_temp - in_temp) / 10
        :epsilon: (sinktemp-30) * 6.34

        :return: speed at which to set the fan (0-100) in multiples of 5.
        """
        if self.fantype == 'Binary':
            fanspeed = 0
            if i_humidity > settings.sethumid:
                fanspeed = 1
            if i_temp > settings.settemp:
                fanspeed = 1
            return fanspeed

        elif self.fantype == 'PWM':
            alpha = -5 * (lightstate - 1)
            beta = 0
            if i_humidity > settings.sethumid:
                beta = 5
            io_delta = o_temp - i_temp  #
            delta_t = settings.settemp - i_temp  # pos values means we want the temp to go up, neg = want temps to go down.
            temp_coef = io_delta * delta_t  # will return positive values if both match
            gamma = 0
            if temp_coef > 0:
                gamma = temp_coef / 10
            epsilon = max(0, (sinktemp - 30) * 6.34)

            omega = alpha + beta + gamma + epsilon
            logger.debug(
                'omega = alpha + beta + gamma + epsilon\n{}(fanspeed) = {}(lights) + {}(humidity) + {}(temp_coef) + {}(heatsink)'.format(
                    omega, alpha, beta, gamma, epsilon))
            fanspeed = min(100, int(round(omega / 5) * 5))
            return fanspeed

    def speed(self, value):
        """Handles the speed of the fans, including master power, on/off."""
        dutycycle = 100.0 - value  # 100 is slow, 0 is fast
        if 0 < value <= 100:
            self.pwm.ChangeDutyCycle(dutycycle)
            GPIO.output(self.powerpin, GPIO.LOW) # power on
            # self.on()
            self.tach = value
            logger.debug('fans set to speed: {}'.format(self.tach))
            # print "ON"
        elif value == 0:
            # self.off()
            GPIO.output(self.powerpin, GPIO.HIGH)  # power off
            self.tach = 0
            logger.debug('fans set to speed: {}'.format(self.tach))
            # print "OFF"
            # if self.lights.state:  #lights.state = 1 means lights are off
            #     GPIO.output(self.powerpin, GPIO.HIGH)  # power off
            # else:
            #     raise ValueError("cannot set speed to 0 when lights are on")
        else:
            logger.error('non-valid fan speed submitted: {}}'.format(value))
            raise ValueError("Speed must be between 0.0-100.0")


    # def on(self):
    #     """switches GPIO pin to LOW/0 - in open state relays, this turns the relay ON."""
    #     GPIO.output(self.powerpin, GPIO.LOW)
    #
    #
    # def off(self):
    #     """ switches GPIO pin to HIGH/1 - in open state relays, this turns the relay OFF."""
    #     GPIO.output(self.powerpin, GPIO.HIGH)

    # def tempcontrol(self, settemp):
    #     while True:
    #         # send temp measurement to PID
    #         # inside PID there will be an if/else clause that sets the min fanspeed if the lights are on
    #         newfanspeed = pid(temp)
    #         self.speed(newfanspeed)
    #

    @property
    def state(self):
        return GPIO.input(self.powerpin)


"""Manual control mode"""
if __name__ == "__main__":
    power = raw_input("Which GPIO pin powers the fan (13)?\n>>>")
    pwm = raw_input("Which pin controls the speed (18)?\n>>>")
    wind = Wind(int(power),int(pwm))
    try:
        while True:
            inputspeed = input("Enter fan speed(0.0-100.0): ")
            try:
                wind.speed(inputspeed)
            except ValueError:
                print "invalid set speed"
            except:
                print "something went wrong."
                break
            else:
                print "New duty cycle = {}".format(inputspeed)

    finally:
        wind.pwm.stop()
        GPIO.cleanup()
        print('PWM stopped, GPIO pins have been cleaned up. Goodbye.')

