# this file will read gcode commands from a file and send them
# one by one over serial to the arduino
# ack we probably want a GUI too right?
# nah i do that later fuck that

import sys, serial
from tkinter import *

# since im doing in terminal for now
# sys.argv is a list with ['ArduinoControl.py', ...]
# so running it like ```python3 ArduinoControl.py path/to/test.gcode``` 
# would make ['ArduinoControl.py','path/to/test.gcode']

# path to gcode file to open
gpath = sys.argv[1]

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
ser.reset_input_buffer()

with open(gpath) as f:
    for line in f:
        ser.write((line + '\n').encode('ascii'))