from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 1.8)
MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins

# lowercase for stepper 2
dir = 16
step = 19
mode = (17, 27, 22)

GPIO.setup(MODE, GPIO.OUT)
GPIO.setup(mode, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
GPIO.output(MODE, RESOLUTION['1/8'])
GPIO.output(mode, RESOLUTION['1/8'])

#step_count = SPR * 32
#delay = .0208 / 32
#GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(dir, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(step, GPIO.OUT)
GPIO.output(DIR, CW)
GPIO.output(dir, CW)

step_count = SPR * 8
delay = .00002

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    GPIO.output(step, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    GPIO.output(step, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIR, CCW)
GPIO.output(dir, CCW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    GPIO.output(step, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    GPIO.output(step, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()