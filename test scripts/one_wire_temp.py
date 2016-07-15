




import RPi.GPIO as GPIO



# GPIO pins connected
temp_sensor_strand = 17
relay1 = 18
relay2  = 27
fan_pwm_1 = 24
fan_pwm_2 = 25

def activate_pin(pin, name, io, initial)