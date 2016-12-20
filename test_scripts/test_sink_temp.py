from sun import Sun
from wind import Wind
from pid import PID
from one_wire_temp import w1therm
from pins import Relay
import logging
from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

logger = logging.getLogger()
logging.basicConfig()

lights = Relay(19,'lights')
# sun = Sun(lights,settings,MAXTEMP)
print 'lights set up on pin 19'
heatsinksensor = w1therm()

fans = Wind(13,18)
print 'fans set up on pin 13'
p = PID(2, 0, 1,0,0,100,0)
print 'PID set up'
p.setPoint(50.0)
print 'PID set point to 50.0'
def main():
    try:
        lights.on()
        print 'lights on'
        while True:
            # read heatsink temps, return max
            listoftemps = []
            temps = heatsinksensor.gettemps()
            for temp in temps:  # temps is a dict: {'28-031655df8bff': 18.625, 'timestamp': datetime.datetime(2016, 11, 11, 22, 47, 35, 344949)}
                if temp == 'timestamp':
                    continue
                else:
                    tempfloat = float(temps[temp])
                    listoftemps.append(tempfloat)
            # feed max temp into PID
            highest_temp = max(listoftemps)
            logger.info('the max temp: %s', str(highest_temp))
            speed_adjustment = p.update(max(listoftemps))
            # get back PID value
            logger.info('fans need to change speed %s amount', str(speed_adjustment))
            # adjust fanspeed
            new_speed = float(fans.tach) + float(speed_adjustment)
            logger.info('speed before adjustment: %s', new_speed)
            if new_speed > 100:
                new_speed = 100
            elif new_speed < 0:
                new_speed = 0
            fans.speed(new_speed)
            logger.info('fan speed: %s',str(new_speed))
            # wait
            sleep(10)
    except:
        logger.exception('stuff')
        lights.off()
        GPIO.cleanup()
        logger.warning("canceled, pins cleaned up")


if __name__ == '__main__':
    main()




# class items:
#     def __init__(self,num):
#         self.num = num
#         print 'items = ', num
#
#     def update(self,value):
#         self.num = value
#
#
# class test1:
#     def __init__(self, number, items):
#         self.number = number
#         self.items = items
#         t1 = Thread(target=self.run_test, )
#         t1.start()
#         print 'started test1'
#         t2 = Thread(target=self.run_test2,)
#         t2.start()
#
#     def run_test(self):
#         for i in range(5):
#             sleep(5)
#             print 'using just the input number: ' + str(self.number)
#
#     def run_test2(self):
#         for i in range(5):
#             sleep(5)
#             print 'using the settings object: ' + str(self.items.num)
#
#
# def main():
#     x = items(10)
#     tester = test1(x.num,x)
#     sleep(1)
#     x.update(100)
#
# if __name__ == '__main__':
#     main()
