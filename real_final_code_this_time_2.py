'''
    TODO
     - check what stepper driver / motor combo we have and 
        write stepper code after each signature thing
     - add button in the GUI to start signing instead of 
        just going automatically
     - add button in the GUI to take in gcode file instead of 
        svg if he already has one read
     - add stop/resume buttons in the GUI for if machine fuck up
        (add listeners that change global vars somewhere maybe? 
        and then check gvar value between each serial cmnd)
'''

# this is the same thing as FINALCODE.py but the dialog that pops up
# has a box for you to set the output filename

from tkinter import *
from tkinter import filedialog
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import os, sys, serial, time
import RPi.GPIO as g
from RpiMotorLib import RpiMotorLib

g.setmode(g.BCM)

window = Tk()
window.title('SVG to Gcode convertir')

# global variables

# path to original gcode file
fpath = ''

# number of signatures to print
nsv = 1

# distance to move pen to toggle writing/not writing
z_amt = 5

# contents of the file as a string
fcontents = 'why am i doing it like this?'


# --------------------------------------

# GCODE FUNCTIONS


# svg >> gcode
def modify():
    global nsv, fpath, z_amt
    ext = ''
    tmp = []
    if os.name == 'nt': # windows
        # modify path
        tmp = fpath.split('/')
        tmp.pop()
        ext = ('/'.join(tmp) + '/')
    else: # linux
        # again
        print('bro')
        tmp = fpath.split('\\')
        tmp.pop()
        ext = ('\\'.join(tmp) + '\\')
		# how many copies we want
    try: 
        # print(num_sigs_var.get())
        nsv = int(num_sigs_var.get())
    except:
        # error output?
        print('number of signatures wasn\'t an int')
        progress.configure(text='Error: # signatures isn\'t a number')

        return
    
    output_name = output_input_var.get()
    
    if not output_name[(len(output_name) - 6):] == '.gcode':
        output_name += '.gcode'
    
	
    progress.configure(text='Progress:\tModifying file')

    curves = parse_file(fpath) # Parse an svg file into geometric curves

    gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
    gcode_compiler.append_curves(curves) 
    gcode_compiler.compile_to_file(ext + output_name, passes=1)

    gcode_file = open(ext + output_name, 'r+')
    gcode_contents = gcode_file.read()
    gcode_file.close()
    gcode_file = open(ext + output_name, 'w')

    # change spindle commands to Z-axis movement
    plorb = gcode_file.split('\n')
    outfile = ''
    for glemp in plorb:
        # spindle is M3 or M4 or M5
        # or M03 M04 M05
        if glemp.split(' ')[0] == 'M3':
            # replace with Z-down
            outfile += 'G91 G0 Z' + str(z_amt) + '\n'
            pass
        elif glemp.split(' ')[0] == 'M4':
            # replace with Z-up
            outfile += 'G91 G0 Z-' + str(z_amt) + '\n'
            pass
        elif glemp.split(' ')[0] == 'M5':
            # replace with Z-up
            outfile += 'G91 G0 Z-' + str(z_amt) + '\n'
            pass
        else:
            outfile += glemp + '\n'

    gcode_file.write(outfile)
    gcode_file.close()
        

    progress.configure(text='Saved to ' + output_name)
    # do not run it automatically immediately after finishing conversion
    # TODO: add something here to be like automatically load in gcode file to other thing
    # do_signage((ext + output_name))



# --------------------------------------

# file explorer
# find file + set global fpath variable
def file_explorer():
    global fpath
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("SVG files",
                                                        "*.svg*"),
                                                       ("all files",
                                                        "*.*")))
    
    selected_file_display.delete('1.0', END)
    selected_file_display.insert(END, filename)
    # print(filename)
    fpath = filename

# --------------------------------------
# CONTORL ARDUINO
ser = ''
pause = False
cst = False
cst2 = False
def do_signage():
    global ser, pause, cst, cst2
    # TODO: read in gfile from StringVar
    gfile = ''
    ser = serial.Serial('dev/ttyACM0', 115200, timeout=1)
    ser.reset_input_buffer()

    with open(gfile) as f:
        for i in range(nsv):
            for line in f:
                ser.write((line + '\n').encode('ascii'))
                # maybe need a delay here to wait for the 
                # machine to move
                if cst:
                    break
            while (pause):
                if cst:
                    cst = False
                if cst2:
                    pause = False

            # im not sure if we need the ~ and ! commands
            # if it's not being sent any commands while
            # the stepper code is running anyway
            if not cst2:
                ser.write(b'!') # pause to run stepper code
                # run stepper code here
                ser.write(b'~') # resume
            else: 
                cst2 = False



# --------------------------------------
# GRAPHICS


#region graphics stuff
selected_file = Label(window, text='Selected file:')
selected_file_display = Text(window, height=1, width=60)
browse_files = Button(window, text='browse files', command=file_explorer)
output_label = Label(window, text='Output filename:')
output_input_var = StringVar(value='output.gcode')
output_input = Entry(window, textvariable=output_input_var, width=60)
num_sigs = Label(window, text='# of copies: ')
num_sigs_var = StringVar(value='1')
enter_num_sigs = Entry(window, textvariable=num_sigs_var, width=66)
start = Button(window, text='Begin', command=modify)
progress = Label(window, text='Progress:\tNot Started')
set_pen_height = Label(window, text='Set pen height (mm):')

sph_amt = StringVar(value='5')
sph_input = Entry(window, textvariable=sph_amt, width=20)

#region shitter functions
def homeit():
    ser.write(b'$H\n')

def estopit():
    ser.write(b'M112\n')

# TODO: add these these commands
def cffit():
    pass

def cfbit():
    pass

def cyclestartit():
    global cst2
    cst2 = True

def cyclestopit():
    global cst, pause
    cst = True
    pause = True
#endregion

home_button = Button(window, text='Home machine', command=homeit)
e_stop = Button(window, text='Emergency Stop', command=estopit)
cf_forward = Button(window, text='Card feeder forwards', command=cffit)
cf_backward = Button(window, text='Card feeder backwards', command=cfbit)
cycle_start = Button(window, text='Start cycle', command=cyclestartit)
cycle_stop = Button(window, text='Stop cycle', command=cyclestopit)

start_sign = Button(window, text='Start', command=do_signage)

''' GUI outline

    selected file:      ______________      |browse|
    output filename:    ______________
    # of signatures:    ______________
                        |begin|             Progress: loading file/modifying file/done
    Set pen height:                         |Home machine|
    ______________      |Estop|             |cycle start|
    |Card feed forward| |C.F. backward|     |cycle stop|
    |quit|              |start signing|
'''

selected_file.grid(row=0, column=0)
selected_file_display.grid(row=0, column=1)
browse_files.grid(row=0, column=2)
output_label.grid(row=1, column=0)
output_input.grid(row=1, column=1)
num_sigs.grid(row=2, column=0)
enter_num_sigs.grid(row=2, column=1)
start.grid(row=3, column=1)
progress.grid(row=3, column=2)
set_pen_height.grid(row=4, column=0)
sph_input.grid(row=5,column=0)
home_button.grid(row=4,column=2)
e_stop.grid(row=6,column=0)
cf_forward.grid(row=5,column=1)
cf_backward.grid(row=6,column=1)
cycle_start.grid(row=5,column=2)
cycle_stop.grid(row=6,column=2)
start_sign.grid(row=7,column=0)
#endregion

window.mainloop()