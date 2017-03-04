from time import sleep
from random import randint
from threading import Thread
import logging
import logging.handlers

LOG_FILENAME = 'deletethis.log'
LOG_LVL = logging.DEBUG

logging_format = "[%(levelname)s] %(name)s %(asctime)s %(message)s"


# Set up a specific logger with our desired output level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1024, backupCount=5)
handler.setLevel(LOG_LVL)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Add a formatter
formatter = logging.Formatter(logging_format)
handler.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(ch)

#
#
# logger = logging.getLogger(__name__)
# # logging.basicConfig(filename='deletethis.log', format=logging_format, level=logging.INFO)
# logger.setLevel(logging.DEBUG)
# # create file handler which logs even debug messages
# fh = logging.FileHandler('deletethis_spam.log')
# fh.setLevel(logging.DEBUG)
# # create console handler with a higher log level
# ch = logging.()
# ch.setLevel(logging.ERROR)
# # create formatter and add it to the handlers
# formatter = logging.Formatter(logging_format)
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # add the handlers to logger
# logger.addHandler(ch)
# logger.addHandler(fh)
#
#


def worker(name):
    try:
        while True:
            sleep(3)
            val = randint(0,5)
            if val == 5:
                raise Exception('Oops!')
            # print('{}: I got {}'.format(name, val))
            logger.info('{}: I got {}'.format(name, val))
    except:
        logger.exception('{} has encountered a 5.'.format(name))


def read(maxattempts):
    """testing a while loop"""
    attempts = 0
    while attempts < maxattempts:
        try:
            val = randint(0, 5)
            if val == 5:
                return val
            raise TypeError('could not read sensor.')

        except TypeError:
            attempts += 1
            sleep(2)
    return "sensor could not be reached after {} attempts.".format(maxattempts)

def main():
    workers = {
        # 'baz': Thread(target=worker2),
        'bar': Thread(target=worker, args=('bar',)),
        'foo': Thread(target=worker, args=('foo',))
    }
    for name in workers:
        workers[name].start()

    while True:
        sleep(1)
        for name in workers:
            if not workers[name].is_alive():
                # print('Main: {} died! Restarting...'.format(name))
                logger.warning('Main: {} died! Restarting...'.format(name))

                workers[name] = Thread(target=worker, args=(name,))
                workers[name].start()


if __name__ == '__main__':

# to test logging uncomment below:
    main()

#to test the while loop uncomment this

    # x = read(3)
    # print x
