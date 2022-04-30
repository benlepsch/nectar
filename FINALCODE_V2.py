# this is the same thing as FINALCODE.py but the dialog that pops up
# has a box for you to set the output filename

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
    gcode_file = open(ext + output_name, 'a')

    # if there's code to insert at the beginning of each loop, can replace the \n in the else statement with code

    gcode_contents = '\n'.join([(x if x != 'G90;' else '\n') for x in gcode_contents.split('\n')])
    for i in range(nsv - 1):
        # gcode_file.write('\n')
        gcode_file.write(gcode_contents)
        
    gcode_file.close()

    progress.configure(text='Saved to ' + output_name)



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
    output filename: ____________
    # of signatures: _______
    |begin|       Progress: loading file/modifying file/done
    |quit|
'''
#region graphics stuff
selected_file = Label(window, text='Selected file:')
selected_file_display = Text(window, height=1, width=60)
browse_files = Button(window, text='browse files', command=file_explorer)
output_label = Label(window, text='Output filename:')
output_input_var = StringVar()
output_input = Entry(window, textvariable=output_input_var, width=60)
num_sigs = Label(window, text='# of copies: ')
num_sigs_var = StringVar()
enter_num_sigs = Entry(window, textvariable=num_sigs_var, width=66)
start = Button(window, text='Begin', command=modify)
progress = Label(window, text='Progress:\tNot Started')
kwit = Button(window, text='Exit', command=window.destroy)

selected_file.grid(row=0, column=0)
selected_file_display.grid(row=0, column=1)
browse_files.grid(row=0, column=2)
output_label.grid(row=1, column=0)
output_input.grid(row=1, column=1)
num_sigs.grid(row=2, column=0)
enter_num_sigs.grid(row=2, column=1)
start.grid(row=3, column=1)
progress.grid(row=3, column=2)
kwit.grid(row=4, column=0)
#endregion

window.mainloop()