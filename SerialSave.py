import csv
import serial
import math
import time
import re
import os
from pathlib import Path
from tkinter import *

state = False  # Global flag
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM5'
data = []
header = ['CO2: ppm', 'TVOC: ppb']
global f
global z

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
    while os.path.exists('datafile%d.csv' % i):
        i += 1
    global filename
    filename = ('datafile%d.csv' % i)

def File():
    FileNameCreator()
    global f
    global z
    f = open(filename, 'w')  #open file, erase contents when writing
    z = csv.writer(f)
    z.writerow(header)
    time.sleep(3)

File()

def ReadWrite():
    ser.write(b'B')
    Bline = ser.readline() #read Data
    line = str(Bline, 'utf-8') #bytes to string conversion
    num = re.findall(r'\d+', line[3:]) #extract important numbers from Data
    res = list(map(int, num)) #maps the data to integers
    if len(res) == 2: #excluding erronious data
        data = res
        print(data) 
        z.writerow(data)

def scanning():
    if state:  # If start button was clicked
        ReadWrite()
    # After 1 second, call scanning again (create a recursive loop)
    root.after(1000, scanning)

def start():
    """Enable scanning by setting the global flag to True."""
    global state
    state = True
    ser.open()

def stop():
    """Stop scanning by setting the global flag to False."""
    global state
    state = False
    ser.close()
    f.close()
    print("COM Closed")

root = Tk()
root.title("COM State")
root.geometry("500x200")

app = Frame(root)
app.grid()

start = Button(app, text="Open COM Port", command=start, fg="green")
stop = Button(app, text="Close COM Port", command=stop, fg="red")

start.grid()
stop.grid()

root.after(1000, scanning)  # After 1 second, call scanning
root.mainloop()

