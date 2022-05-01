from time import sleep
import RPi.GPIO as g
import sys, serial


CW = 1
CCW = 0
SPR = 200
RES = {'Full': (0, 0, 0),
        'Half': (1, 0, 0),
        '1/4': (0, 1, 0),
        '1/8': (1, 1, 0),
        '1/16': (0, 0, 1),
        '1/32': (1, 0, 1)}

step_count = SPR * 8
delay = 0.00002

dir1 = 20
step1 = 21
mode1 = (14, 15, 18)

dir2 = 16
step2 = 19
mode2 = (17, 27, 22)

g.setup(mode1, g.OUT)
g.setup(mode2, g.OUT)

g.output(mode1, RES['1/8'])
g.output(mode2, RES['1/8'])

g.setmode(g.BCM)

g.setup(dir1, g.OUT)
g.setup(dir2, g.OUT)
g.setup(step1, g.OUT)
g.setup(step2, g.OUT)

g.output(dir1, CW)
g.output(dir2, CW)

# also run homing cycle
s = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
s.write(b'$H\n')

for x in range(step_count):
    g.output(step1, g.HIGH)
    g.output(step2, g.HIGH)
    sleep(delay)
    g.output(step1, g.LOW)
    g.output(step2, g.LOW)
    sleep(delay)

sleep(0.5)
g.output(dir1, CCW)
g.output(dir2, CCW)

for x in range(step_count):
    g.output(step1, g.HIGH)
    g.output(step2, g.HIGH)
    sleep(delay)
    g.output(step1, g.LOW)
    g.output(step2, g.LOW)
    sleep(delay)