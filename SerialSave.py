import csv
import serial
import math
import time
import re
import os
from pathlib import Path
from tkinter import *

state = True  # Global flag
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM5'
i = 0
data = []
header = ['CO2: ppm', 'TVOC: ppb']

while os.path.exists('datafile%d.csv' % i):
    i += 1
filename = ('datafile%d.csv' % i)


def File():
    global f
    f = csv.writer(open(filename, "w")) #open file, erase contents when writing
    f.writerow(header)
    time.sleep(3)

File ()

def ReadWrite():
    ser.write(b'B')
    Bline = ser.readline() #read Data
    line = str(Bline, 'utf-8') #bytes to string conversion
    num = re.findall(r'\d+', line[3:]) #extract important numbers from Data
    res = list(map(int, num)) #maps the data to integers
    if len(res) == 2: #excluding erronious data
        data = res
        print(data) 
        f.writerow(data)

def scanning():
    if state:  # Only do this if the Stop button has not been clicked
        try:
            ser.open()# Open com port
        except:
            print("error opening COM Port")
        print('Serial Port is open : ' + ser.name)
        ReadWrite()

    # After 1 second, call scanning again (create a recursive loop)
    root.after(1000, scanning)

def start():
    """Enable scanning by setting the global flag to True."""
    global state
    state = True

def stop():
    """Stop scanning by setting the global flag to False."""
    global state
    state = False

root = Tk()
root.title("COM State")
root.geometry("500x500")

app = Frame(root)
app.grid()

start = Button(app, text="COM Port Open", command=start)
stop = Button(app, text="COM Port Closed", command=stop)

start.grid()
stop.grid()

root.after(1000, scanning)  # After 1 second, call scanning
root.mainloop()
print(state)

