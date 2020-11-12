import csv
import serial
import math
import time
import re
import os
from pathlib import Path

i = 0
data = []
header = ['CO2: ppm', 'TVOC: ppb']
while os.path.exists('datafile%d.csv' % i):
    i += 1
filename = ('datafile%d.csv' % i)

try:
    ser = serial.Serial('COM5', 115200) # Open com port
except:
    print("error opening COM Port")
print('Serial Port is open : ' + ser.name)

with open(filename, "w") as new_file: #open file, erase contents when writing
    csv_writer = csv.writer(new_file)
    csv_writer.writerow(header)
    time.sleep(3)
    ser.write(b'B')
    o = 0
    while ser.is_open:
        Bline = ser.readline() #read Data
        line = str(Bline, 'utf-8') #bytes to string conversion
        num = re.findall(r'\d+', line[3:]) #extract important numbers from Data
        res = list(map(int, num)) #maps the data to integers
        if len(res) == 2: #excluding erronious data
            data = res
            print(data) 
        csv_writer.writerow(data) #save data to csv
        o += 1
        if o > 41600: #counter
            print('\nThis is the end of the file\n')
            ser.close()
            break
