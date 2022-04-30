# this program will control the stepper motor or whatever 
# is connected directly to the pi

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM) # uses labeled pins on the pi ribbon cable connector

'''
# to setup / control pins do like this

led_pin = 17
gpio.setup(led_pin, gpio.OUT)
gpio.output(led_pin, True)
'''