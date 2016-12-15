import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)  # for using the names of the pins
GPIO.setwarnings(True)  # set to false if the warnings bother you, helps troubleshooting

logger = logging.getLogger(__name__)

class Wind:
    """This will house all of functions used to control the fans"""
    def __init__(self, powerpin, speedpin, speed = 0):
        self.powerpin = powerpin
        GPIO.setup(powerpin, GPIO.OUT, initial=1)
        GPIO.setup(speedpin, GPIO.OUT)
        self.pwm = GPIO.PWM(speedpin, 25000) # 25 Kilohertz is inaudible to human ears
        self.pwm.start(speed)
        self.tach = speed
        logger.info('fans initiated.  Power on pin {}, speed control PWM on pin {}'.format(self.powerpin,self.pwm))


    def speed(self, value):
        """Handles the speed of the fans, including master power, on/off."""
        dutycycle = 100.0 - value  # 100 is slow, 0 is fast
        if 0 < value <= 100:
            self.pwm.ChangeDutyCycle(dutycycle)
            GPIO.output(self.powerpin, GPIO.LOW) # power on
            # self.on()
            self.tach = value
            logger.debug('fans set to speed: %s' %str(self.tach))
            # print "ON"
        elif value == 0:
            # self.off()
            GPIO.output(self.powerpin, GPIO.HIGH)  # power off
            self.tach = 0
            logger.debug('fans set to speed: %s' % str(self.tach))
            # print "OFF"
            # if self.lights.state:  #lights.state = 1 means lights are off
            #     GPIO.output(self.powerpin, GPIO.HIGH)  # power off
            # else:
            #     raise ValueError("cannot set speed to 0 when lights are on")
        else:
            logger.error('non-valid fan speed submitted: %s' % str(value))
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
                print "New duty cycle = %s"%inputspeed

    finally:
        wind.pwm.stop()
        GPIO.cleanup()
        print('PWM stopped, GPIO pins have been cleaned up. Goodbye.')

