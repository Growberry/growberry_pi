
import logging
import datetime
# import pytz
#
#
# now = datetime.datetime.now(tz=pytz.timezone('US/Pacific')).time()
#
# # utcnow = datetime.datetime.utcnow().time().astimezone('US/Pacific')
#
# user_tz = "1"
#
# def usertest():
#     user_entry = datetime.datetime.strptime(raw_input("what time do you want the lights to come on?\n>>> "),'%H%M').time()
#     # datetime.strptime(self.settings['sunrise'], '%H%M').time()
#     print user_entry
#     user_entry_utc = user_entry
#
#
#
# print now
# # print utcnow
#
# usertest()
# # #
# # for tz in pytz.all_timezones:
# #     print tz
#
#
# import threading
# import time
#
# def do_work(id, active):
#     print("I am thread", id)
#     while active:
#         print("I am thread {} doing something".format(id))
#         time.sleep(2)
#         # if stop():
#         #     print("  Exiting loop.")
#         #     break
#     print("Thread {}, signing off".format(id))
#
#
# def main():
#     active = True
#     workers = []
#
#     t1 = threading.Thread(target=do_work, args=('t1', lambda: active))
#     workers.append(t1)
#     t1.start()
#     t2 = threading.Thread(target=do_work, args=('t2', lambda: active))
#     workers.append(t2)
#     t2.start()
#     time.sleep(12)
#     # except(KeyboardInterrupt):
#     print('main: interrupted. stopping the threads...')
#     active = False
#     for worker in workers:
#         worker.join()
#
#     # finally:
#     print('Finished.')

class testDec(object):
    def __init__(self, speed):
        self._speed = speed
        self._log = 'log'

    @property
    def speed(self):
        print 'called getter'
        return self._speed

    @speed.setter
    def x(self, value):
        print 'called setter'
        self._speed = value
        self.testfunc(value, self._speed)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self._log = self._path + '\log'

    def testfunc(self, x,y):
        print "adding the numbers %s and %s"%(x,y)
        z = x + y
        print z

# t = testDec(30)
# print t.speed
# t.x = 99
# print t.x
# t.path = 'new'
# print t.path
# print t._log

#
# logger = logging.getLogger(__name__)
logging_format = "[%(levelname)s] %(name)s %(asctime)s %(message)s"
#
logging.basicConfig(format=logging_format, level=logging.DEBUG)
#
# logger.info('test')

def lightcontrol(rise, length):
    """
    determines if artificial lights should be on, or off.
    :param rise: datetime.time(h,m,s)
    :param length: integer number of hours
    :return: lights activate or deactivate.
    """
    length_delta = datetime.timedelta(hours=length)
    sunrise = datetime.datetime.combine(datetime.date.today(),rise)
    sunset = sunrise + length_delta
    set = sunset.time()
    now = datetime.datetime.now()
    tomorrow = datetime.datetime.now() + datetime.timedelta(hours=24)
    midnight = datetime.datetime.combine(tomorrow.date(), datetime.time(0,0,0))
    logging.debug('midnight: {}'.format(midnight))
    if sunrise <= midnight <= sunset:
        logging.debug('day spans midnight')
        if set <= now.time() <= rise:
            logging.debug(
                '\nsunrise:  {}\nsunset: {}\nnow: {}\nlights OFF.'.format(rise, set, datetime.datetime.now().time()))
        else:
            logging.debug(
                '\nsunrise:  {}\nsunset: {}\nnow: {}\nlights ON.'.format(rise, set, datetime.datetime.now().time()))
    else:
        if rise <= now.time() <= set:
            logging.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights ON.'.format(sunrise, sunset, datetime.datetime.now()))
        else:
            logging.debug('\nsunrise:  {}\nsunset: {}\nnow: {}\nlights OFF.'.format(sunrise, sunset, datetime.datetime.now()))



if __name__ == '__main__':
    time = datetime.time(22,0,0)
    lightcontrol(time,22)

