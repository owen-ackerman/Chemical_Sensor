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

frequency = 1000 #scanning and data collection frequency, miliseconds
state1 = False  # Global flag
state2 = False
ser1 = serial.Serial() # Initialize serial port
ser2 = serial.Serial()
ser1.baudrate = 115200 # Set baud rate
ser2.baudrate = 115200
ser1.port = 'COM8'
ser2.port = 'COM3' #set com port
data1 = [] # initialize variable data as list
data2 = []
header = ['CO2: ppm,', 'TVOC: ppb,', 'Time'] #initialize the header list
global f # variable set to the csv file
global z # variable set to the csv modifier (writer etc.)

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

def FileNameCreator1():
    global i
   
    i = 0 
    while os.path.exists(ser1.name + 'Data%d.csv' % i): #checks if the filename exists
        i += 1 #increments if file name exists
    global filename1
    filename1 = (ser1.name + 'Data%d.csv' % i) #sets the filename with the modified incrementor
    
def FileNameCreator2():
    global j
    j = 0
    while os.path.exists(ser2.name + 'Data%d.csv' % j): #checks if the filename exists
        j += 1 #increments if file name exists
    global filename2
    filename2 = (ser2.name + 'Data%d.csv' % j) #sets the filename with the modified incrementor



def File1():
    FileNameCreator1()
    global f1
    global z1
    f1 = open(filename1, 'w')  #open file, erase contents when writing
    z1 = csv.writer(f1) #tells the csv.writer which function to modify
    z1.writerow(header) #writes the list header in the csv file
   
def File2():
    FileNameCreator2()
    global f2
    global z2
    f2 = open(filename2, 'w')
    z2 = csv.writer(f2)
    z2.writerow(header)

def ReadWrite1():
    ser1.write(b'B') #sets the incoming information as bytes
    Bline1 = ser1.readline() #read Data 
    line1 = str(Bline1, 'utf-8') #bytes to string conversion
    num1 = re.findall(r'\d+', line1[3:]) #extract important numbers from Data
    res1 = list(map(int, num1)) #maps the data to integers
    if len(res1) == 2: #excluding erronious data
        data1 = res1
        now1 = datetime.now()
        seconds1 = (now1 - now1.replace(hour=0, minute=0, second=0, microsecond=0)).seconds
        data1.append(seconds1)
        print(data1) #prints data to terminal
        z1.writerow(data1) #write data to csv file
        text_area1.insert(INSERT, data1)
        text_area1.insert(INSERT, '\n')
        text_area1.yview('end')
    
        
def ReadWrite2():
    ser2.write(b'B')
    Bline2 = ser2.readline()
    line2 = str(Bline2, 'utf-8')
    num2 = re.findall(r'\d+', line2[3:])
    res2 = list(map(int, num2))
    if len(res2) == 2:
        data2 = res2
        now2 = datetime.now()
        seconds2 = (now2 - now2.replace(hour=0, minute=0, second=0, microsecond=0)).seconds
        data2.append(seconds2)
        print(data2)
        z2.writerow(data2)
        text_area2.insert(INSERT, data2)
        text_area2.insert(INSERT, '\n')
        text_area2.yview('end')

def scanning():
    if state1:  # If start button was clicked
        ReadWrite1()

    if state2:
        ReadWrite2()
    # After 1 second, call scanning again (create a recursive loop)
    root.after(frequency, scanning)

def start1():
    """Enable scanning by setting the global flag to True."""
    File1()
    ser1.open() #opens serial port
    print(ser1.name + "opened")
    global state1
    state1 = True
    
    

def start2():
    """Enable scanning by setting the global flag to True."""
    File2()
    ser2.open() #opens serial port
    print(ser2.name + "opened")
    global state2
    state2 = True
    

def stop1():
    """Stop scanning by setting the global flag to False."""
    global state1
    state1 = False
    ser1.close() #closes serial port
    f1.close() #closes csv file
    print(ser1.name + " Closed")

def stop2():
    """Stop scanning by setting the global flag to False."""
    global state2
    state2 = False
    ser2.close() #closes serial port
    f2.close() #closes csv file
    print(ser2.name + " Closed")

root = Tk() #creates tk gui
root.title("COM State") #title 
root.geometry("600x500") #window size

start1 = Button(text="Open:" + ser1.name, command=start1, fg="green") #buttons widget.
stop1 = Button(text="Close:" + ser1.name, command=stop1, fg="red")
start2 = Button(text="Open:" + ser2.name, command=start2, fg="green")
stop2 = Button(text="Close:" + ser2.name, command=stop2, fg="red")

TestCOM1 = Button(text="Test:" + ser1.name, command= TestCOM1, fg="purple")
TestCOM2 = Button(text="Test:" + ser2.name, command= TestCOM2, fg="purple")

start1.grid(column = 0, row = 0) #places buttons with the .grid() function
stop1.grid(column = 1, row = 0, sticky=W)
start2.grid(column = 2, row = 0)
stop2.grid(column = 3, row = 0, sticky=W)
TestCOM1.grid(column=4, row =0)
TestCOM2.grid(column=4, row = 1)

w1 = Label(root,  
         text = "ScrolledText Widget 1",  
         font = ("Times New Roman", 12),  
         background = 'blue', 
         padx = 40, 
         foreground = "white")
w1.grid(row = 2, columnspan=2, sticky=W)

w2 = Label(root,  
         text = "ScrolledText Widget 2",  
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
text_area1.insert(INSERT, header)
text_area1.insert(INSERT, '\n')
text_area2.insert(INSERT, header)
text_area2.insert(INSERT, '\n')

# Making the text read only 
#text_area.configure(state ='disabled') 
  # After 1 second, call scanning
root.after(1000, scanning)
root.mainloop()
