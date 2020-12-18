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


global seconds #timestamp for data collection
global data1, data2 #incoming data from sensor 1 and sensor 2

frequency = 1000 #scanning and data collection frequency, miliseconds
state = False
state1 = False  # button flag
state2 = False # Button flag

ser1 = serial.Serial() # Initialize serial port
ser2 = serial.Serial()
ser1.baudrate = 115200 # Set baud rate
ser2.baudrate = 115200
ser1.port = 'COM5'
ser2.port = 'COM7' #set com port
data1 = [] # initialize variable data as list
data2 = [] #
header = ['Time Stamp', 'Data Source ID','CO2: ppm,', 'TVOC: ppb,', 'Data Source ID','CO2: ppm,', 'TVOC: ppb,'] #initialize the header list
SinglePortHeader = ['Time Stamp', 'Data Source ID','CO2: ppm,', 'TVOC: ppb,']
Scrolling_Header = ['Time Stamp', 'CO2: ppm,', 'TVOC: ppb,']


def TestCOM1():
    try:
        ser1.open()# Open com port
        print('Port: ' + ser1.name + ' connection secured')
        ser1.close()
    except:
        print("error securing Port: " + ser1.name)

def TestCOM2():
    try:
        ser2.open()
        print('Port: ' + ser2.name + ' connection secured')
        ser2.close()
    except:
        print("error securing Port: " + ser2.name)

TestCOM1()
TestCOM2()

def FileNameCreator():
    global i
    i = 0 
    x = datetime.now()
    y = (x.strftime("%b") + "_" + x.strftime("%d") + "_" + x.strftime("%Y"))
    while os.path.exists(y + 'Data%d.csv' % i): #checks if the filename exists
        i += 1 #increments if file name exists
    global filename
    filename = (y + 'Data%d.csv' % i) #sets the filename with the modified incrementor


def DiPortFile():
    FileNameCreator()
    global f
    global z
    f = open(filename, 'w')  #open file, erase contents when writing
    z = csv.writer(f) #tells the csv.writer which function to modify
    z.writerow(header) #writes the list header in the csv file

def File1():
    FileNameCreator()
    filename1 = ser1.name + filename
    global f1
    global z1
    f1 = open(filename1, 'w')
    z1 = csv.writer(f1)
    z1.writerow(SinglePortHeader)

def File2():   
    FileNameCreator()
    filename2 = ser2.name + filename
    global f2
    global z2
    f2 = open(filename2, 'w')
    z2 = csv.writer(f2)
    z2.writerow(SinglePortHeader)

def Read1():
    global data1
    ser1.write(b'B') #sets the incoming information as bytes
    Bline = ser1.readline() #read Data 
    line = str(Bline, 'utf-8') #bytes to string conversion
    num = re.findall(r'\d+', line[3:]) #extract important numbers from Data
    res = list(map(int, num)) #maps the data to integers
    if len(res) == 2: #excluding erronious data
        data1 = res
        text_area1.insert(INSERT, data1)
        text_area1.insert(INSERT, '\n')
        text_area1.yview('end')
        data1.insert(0, ser1.name)
        
        
def Read2():
    global data2
    ser2.write(b'B')
    Bline = ser2.readline()
    line = str(Bline, 'utf-8')
    num = re.findall(r'\d+', line[3:])
    res = list(map(int, num))
    if len(res) == 2:
        data2 = res
        text_area2.insert(INSERT, data2)
        text_area2.insert(INSERT, '\n')
        text_area2.yview('end')
        data2.insert(0, ser2.name)

def Time():
    global seconds
    now = datetime.now()
    seconds = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds

def CombineWrite():
    global data1, data2
    WholeData = data1 + data2 
    WholeData.insert(0, seconds)
    z.writerow(WholeData)
    print(WholeData)

def Data1Write():
    global data1
    data1.insert(0, seconds)
    z1.writerow(data1)
    print(data1)

def Data2Write():
    global data2
    data2.insert(0, seconds)
    z2.writerow(data2)
    print(data2)

def scanning():
    
    if state:  # If start button was clicked
        Read1()
        Time()
        Read2()
        CombineWrite()
        if state1:
            text_area1.insert(INSERT, 'please do not open' + ser1.name + 'while diPort is running')
            text_area1.insert(INSERT, '\n')
        if state2:
            text_area2.insert(INSERT, 'please do not open' + ser2.name + 'while diPort is running')
            text_area2.insert(INSERT, '\n')

    if state1:
        Read1()
        Time()
        Data1Write()

    if state2:
        Read2()
        Time()
        Data2Write()
    
    # After 1 second, call scanning again (create a recursive loop)
    root.after(frequency, scanning)

def start():
    """Enable scanning by setting the global flag to True."""
    DiPortFile()
    ser1.open() #opens serial port
    ser2.open()
    print(ser1.name + " Opened")
    print(ser2.name + " Opened")
    global state
    state = True
    
def stop():
    """Stop scanning by setting the global flag to False."""
    global state
    state = False
    ser1.close() #closes serial port
    ser2.close()
    f.close() #closes csv file
    print(ser1.name + " Closed")
    print(ser2.name + " Closed")

def start1():
    global state1
    state1 = True
    ser1.open()
    print(ser1.name + ' Opened')
    File1()

def stop1():
    global state1
    state1 = False
    ser1.close()
    f1.close()
    print(ser1.name + " Closed")

def start2():
    global state2
    state2 = True
    ser2.open()
    print(ser2.name + ' Opened')
    File2()

def stop2():
    global state2
    state2 = False
    ser2.close()
    f2.close()
    print(ser2.name + " Closed")


root = Tk() #creates tk gui
root.title("COM State") #title 
root.geometry("600x500") #window size

start = Button(text="DiPorts Open", command=start, fg="green")
stop = Button(text="DiPorts Close", command=stop, fg="red")
start1 = Button(text="Open:" + ser1.name, command=start1, fg="green") #buttons widget.
stop1 = Button(text="Close:" + ser1.name, command=stop1, fg="red")
start2 = Button(text="Open:" + ser2.name, command=start2, fg="green")
stop2 = Button(text="Close:" + ser2.name, command=stop2, fg="red")

TestCOM1 = Button(text="Test:" + ser1.name, command= TestCOM1, fg="purple")
TestCOM2 = Button(text="Test:" + ser2.name, command= TestCOM2, fg="purple")

start.grid(column = 0, row = 0)
stop.grid(column = 1, row = 0)
start1.grid(column = 0, row = 1) #places buttons with the .grid() function
stop1.grid(column = 1, row = 1, sticky=W)
start2.grid(column = 2, row = 1)
stop2.grid(column = 3, row = 1, sticky=W)
TestCOM1.grid(column=2, row =0)
TestCOM2.grid(column=3, row = 0)

w1 = Label(root,  
         text = ser1.name + " Output",  
         font = ("Times New Roman", 12),  
         background = 'blue', 
         padx = 40, 
         foreground = "white")
w1.grid(row = 2, columnspan=2, sticky=W)

w2 = Label(root,  
         text = ser2.name + " Output",  
         font = ("Times New Roman", 12),  
         background = 'purple', 
         padx = 40, 
         foreground = "white")
w2.grid(column = 2, row = 2, columnspan=2, sticky=W)

text_area1 = st.ScrolledText(root, 
                            width = 26, 
                            height = 20,  
                            font = ("Times New Roman", 
                                    12)) 

text_area2 = st.ScrolledText(root, 
                            width = 26, 
                            height = 20,  
                            font = ("Times New Roman", 
                                    12)) 
                                
text_area2.grid(row = 3, column = 2, pady = 0, padx = 0, columnspan = 2) 
text_area1.grid(row = 3, column = 0, pady = 0, padx = 0, columnspan = 2)


#text_area.configure(font=("Arial", 10))
text_area1.insert(INSERT, Scrolling_Header)
text_area1.insert(INSERT, '\n')
text_area2.insert(INSERT, Scrolling_Header)
text_area2.insert(INSERT, '\n')

# Making the text read only 
#text_area.configure(state ='disabled') 
  # After 1 second, call scanning
root.after(1000, scanning)
root.mainloop()
