import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

#define GPIO pins
direction= 22 # Direction (DIR) GPIO Pin
step = 23 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
mymotortest = RpiMotorLib.A4988Nema(direction, step, (14,15,18), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

###########################
# Actual motor control
###########################
#

GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor

# see comments below for what each parameter does
mymotortest.motor_go(False, 'Full', 20, .0005, False, .05)
time.sleep(1)

# for ii in range(10):
#     mymotortest.motor_go(dir_array[ii%2], # False=Clockwise, True=Counterclockwise
#                          "Full" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
#                          200, # number of steps
#                          .0005, # step delay [sec]
#                          False, # True = print verbose output 
#                          .05) # initial delay [sec]
#     time.sleep(1)

GPIO.cleanup()