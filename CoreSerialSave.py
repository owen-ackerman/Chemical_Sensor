'''
test()
This function takes the serial class initialized as a variable for an input and outputs true or false
True means serial port was opened and a line was read from serial port. False means port couldn't be
opened.

SerialPortPrint():
This function takes the serial class initialized as a variable for an input. It then processes the
raw input data and outputs a list of 2 integers [CO2: PPM, TVOC: PPB].

The main logic of this program asks if test(ser) is true, if this is true it loops and prints the
SerialPortPrint() function along with a delay function for the frequency of reading.

*Note*
In order to close the serial port, ser.close() must be called. So this mechanism must be built in. 

For testing purposes, you may unplug and plug back in microcontroler to simulate ser.close()

'''

import serial
import math
import time
import re

frequency = 1 #data read frequency in seconds
ser = serial.Serial() #initiate class serial as variable serial
ser.port = 'COM5' # Set com port
ser.baudrate = 9600 # Set baud rate

def test(self):
    try:
        self.open()# Open com port
        print('Port: ' + self.name + ' opened')
        
    except:
        print("error securing Port: " + self.name)
        return False
        
    if len(self.readline()) > 0: #read line test
        return True

def SerialPortPrint(self):
    self.write(b'B') #sets the incoming information as bytes
    raw = self.readline() #read Data 
    string = str(raw, 'utf-8') #bytes to string conversion
    importantString = re.findall(r'\d+', string[3:]) #extract important numbers from Data
    mappedString = list(map(int, importantString)) #maps the data to integers
    if len(mappedString) == 2: #excluding erronious data
        return mappedString

if test(ser): # if the test was sucessful, start the loop
    while True: #infinate loop
        print(SerialPortPrint(ser)) #read data function
        time.sleep(frequency) #time delay
