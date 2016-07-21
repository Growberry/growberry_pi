#!/usr/bin/python
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pin_num = int(sys.argv[1])
GPIO.setup(pin_num, GPIO.OUT)
my_pwm = GPIO.PWM(pin_num, 25000)
my_pwm.start(0)
try:
    while True:
        speed =input("Enter fan speed(0.0-100.0): ")
        print speed
        print type(speed)
        try: 
            new_duty = 100.0 - speed
            my_pwm.ChangeDutyCycle(new_duty)
        except:
            break
            print "broken"
        else:
            print("New duty cycle = ",new_duty)

finally:
    print('Goodbye.')
    my_pwm.stop()
    GPIO.cleanup()
