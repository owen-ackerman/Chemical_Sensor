import csv
import os
import time
header = ['CO2: ppm', 'TVOC: ppb']

def FileNameCreator():
    global i
    i = 0
    while os.path.exists('datafile%d.csv' % i):
        i += 1
    global filename
    filename = ('datafile%d.csv' % i)
    print(i)

def File():
    FileNameCreator()
    global f
    f = open(filename, 'w')
    global z #open file, erase contents when writing
    z = csv.writer(f)
    z.writerow(header)
    time.sleep(3)

File()


f.close()

