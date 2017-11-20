import Adafruit_DHT
from pins import Sensor
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

ext_sense = Sensor(23, Adafruit_DHT.DHT22, 'external')
in_sense = Sensor(17, Adafruit_DHT.DHT22, 'internal')

try:
    headers = ['datetime.timestamp', 'in_temp', 'ex_temp', 'in_humid', 'ex_humid']
    print '\t'.join(headers)
    while True:
        data = {}
        for sensor in Sensor.array:
            reading = sensor.read
            data.update(reading)
        #print data
        row = [data['internal']['timestamp'],data['internal']['temp'],data['external']['temp'],data['internal']['humidity'],data['external']['humidity']]
        str_row = [str(x) for x in row]
        print "\t".join(str_row)
        sleep(5)
finally:
    GPIO.cleanup()
    print "GPIO pins cleaned up. Goodbye."

