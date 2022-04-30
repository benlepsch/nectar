'''
    POTENTIAL ISSUES

    - the gcode output file uses M5/M3 to stop/start the spindle -- if this doesn't work for the pen up/down
    we can parse code with python and add Z-commands to the lines before/after these instead, but not sure
    what values would be needed for those

    - the svg to gcode library doesn't seem to have a stop command at the end of the file so we should be good
    to just copy/paste the whole thing for each signature

    - not sure how to add things to feed in new papers for new signatures


'''

from tkinter import *
from tkinter import filedialog
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
import os

window = Tk()
window.title('SVG to Gcode convertir')

# global variables

# path to original gcode file
fpath = ''

# number of signatures to print
nsv = 1

# contents of the file as a string
fcontents = 'why am i doing it like this?'

# --------------------------------------

# GCODE FUNCTIONS


# svg >> gcode
def modify():
    global nsv, fpath
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
	
    progress.configure(text='Progress:\tModifying file')

    curves = parse_file(fpath) # Parse an svg file into geometric curves

    gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
    gcode_compiler.append_curves(curves) 
    gcode_compiler.compile_to_file(ext + "output.gcode", passes=1)

    gcode_file = open(ext + 'output.gcode', 'r+')
    gcode_contents = gcode_file.read()
    gcode_file.close()
    gcode_file = open(ext + 'output.gcode', 'a')

    # if there's code to insert at the beginning of each loop, can replace the \n in the else statement with code

    gcode_contents = '\n'.join([(x if x != 'G90;' else '\n') for x in gcode_contents.split('\n')])
    for i in range(nsv - 1):
        # gcode_file.write('\n')
        gcode_file.write(gcode_contents)
        
    gcode_file.close()

    progress.configure(text='Saved to output.gcode')



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
# GRAPHICS

'''
    selected file: ______________  |browse|
    # of signatures: _______
    |begin|       Progress: loading file/modifying file/done
    |quit|
'''

selected_file = Label(window, text='Selected file:')
selected_file_display = Text(window, height=1, width=60)
browse_files = Button(window, text='browse files', command=file_explorer)
num_sigs = Label(window, text='# of copies: ')
num_sigs_var = StringVar()
enter_num_sigs = Entry(window, textvariable=num_sigs_var, width=66)
start = Button(window, text='Begin', command=modify)
progress = Label(window, text='Progress:\tNot Started')
kwit = Button(window, text='Exit', command=window.destroy)

selected_file.grid(row=0, column=0)
selected_file_display.grid(row=0, column=1)
browse_files.grid(row=0, column=2)
num_sigs.grid(row=1, column=0)
enter_num_sigs.grid(row=1, column=1)
start.grid(row=2, column=1)
progress.grid(row=2, column=2)
kwit.grid(row=3, column=0)

window.mainloop()