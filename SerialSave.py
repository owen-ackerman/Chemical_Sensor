'''
This program opens a GUI with 2 buttons that open and close the serial port. 
When the open button is pressed, the serial port is opened and data is both
shown on the terminal and written to a new csv file created with an 
incrementing variable i. When the close button is pressed, the file and serial
port are closed.

FLOW OF EXICUTION: globals are initialized, "state" a boolean variable that 
determines when the serial port is opened and closed. Then the serial
port, baud rate, and com port as well as the header list and data list used for
the csv file. Then the TestCOM() function is called, this opens the com port,
tests it, then closes the port. Then the File() function is called, which calls
the FileNameCreator() function which creates a new filename via the i incrementor. 
Then the File() function creates a new file as filename and write the header 
inside the file. Then the Tk() funciton is called which creates a tkinter window
that is the GUI. The title, size of window. The widget frame that sets a space
where the widget buttons will go. The grid function which will determine exactly
where the buttons will go. Then the buttons are made, and placed with .grid() 
Then the mainloop() is called which waits for user input, proccesses it and breaks
the loop if the main window is destroyed. 
The start button calls the function Start() which sets the boolean state
to True and opens the serial port. the stop button calls the function stop() which
sets the boolean state to False, closes the com port, and closes the .csv file.
Then the scanning() function is called 
by the after() function. scanning function checks boolean state, if True, it runs 
the ReadWrite() function. and reguardless of boolean state, the scanning function 
calls itself again after 1 second through the after() function. The ReadWrite()
function sets the type of information coming in as bytes, then reads the serial 
port and saves as variable. Then that data is converted to a string.
Now the numbers are strings, so the strings are mapped to equivalent integers and 
stored as a list. then the desireable data (2 sets of numbers) are extracted and 
stored the the .csv file.


!!Thanks for reading!!
'''
import csv
import serial
import math
import time
import re
import os
from pathlib import Path
from tkinter import *
import tkinter.scrolledtext as st 
from datetime import datetime
from time import sleep

frequency = 5000 #scanning and data collection frequency, miliseconds
state = False  # Global flag
ser = serial.Serial() # Initialize serial port
ser.baudrate = 115200 # Set baud rate
ser.port = 'COM5' #set com port
data = [] # initialize variable data as list
header = ['CO2: ppm', 'TVOC: ppb', 'Time'] #initialize the header list
global f # variable set to the csv file
global z # variable set to the csv modifier (writer etc.)

def TestCOM():
    try:
        ser.open()# Open com port
        print('Port: ' + ser.name + ' connection secured')
        ser.close()
    except:
        print("error securing COM Port")

TestCOM()

def FileNameCreator():
    global i
    i = 0 
    while os.path.exists('datafile%d.csv' % i): #checks if the filename exists
        i += 1 #increments if file name exists
    global filename
    filename = ('datafile%d.csv' % i) #sets the filename with the modified incrementor

def File():
    FileNameCreator()
    global f
    global z
    f = open(filename, 'w')  #open file, erase contents when writing
    z = csv.writer(f) #tells the csv.writer which function to modify
    z.writerow(header) #writes the list header in the csv file
    time.sleep(3) 

File()

def ReadWrite():
    ser.write(b'B') #sets the incoming information as bytes
    Bline = ser.readline() #read Data
    line = str(Bline, 'utf-8') #bytes to string conversion
    num = re.findall(r'\d+', line[3:]) #extract important numbers from Data
    res = list(map(int, num)) #maps the data to integers
    if len(res) == 2: #excluding erronious data
        data = res
        now = datetime.now()
        seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds
        #print(seconds)
        data.append(seconds)
        print(data) #prints data to terminal
        z.writerow(data) #write data to csv file
        text_area.insert(INSERT, data)
        text_area.insert(INSERT, '\n')
        

def scanning():
    if state:  # If start button was clicked
        ReadWrite()
    # After 1 second, call scanning again (create a recursive loop)
    root.after(frequency, scanning)

def start():
    """Enable scanning by setting the global flag to True."""
    global state
    state = True
    ser.open() #opens serial port

def stop():
    """Stop scanning by setting the global flag to False."""
    global state
    state = False
    ser.close() #closes serial port
    f.close() #closes csv file
    print("COM Closed")

root = Tk() #creates tk gui
root.title("COM State") #title 
root.geometry("250x500") #window size

start = Button(text="Open COM Port", command=start, fg="green") #buttons widget.
stop = Button(text="Close COM Port", command=stop, fg="red")

start.grid(column = 0, row = 0) #places buttons with the .grid() function
stop.grid(column = 1, row = 0, sticky=W)

w = Label(root,  
         text = "ScrolledText Widget",  
         font = ("Times New Roman", 12),  
         background = 'blue', 
         padx = 40, 
         foreground = "white")
w.grid(row = 1, columnspan=2, sticky=W)

text_area = st.ScrolledText(root, 
                            width = 26, 
                            height = 20,  
                            font = ("Times New Roman", 
                                    12)) 
  
text_area.grid(column = 0, pady = 4, padx = 3, columnspan = 2)
#text_area.configure(font=("Arial", 10))
text_area.insert(INSERT, header)
text_area.insert(INSERT, '\n')

# Making the text read only 
#text_area.configure(state ='disabled') 
  # After 1 second, call scanning
root.after(1000, scanning)
root.mainloop()
