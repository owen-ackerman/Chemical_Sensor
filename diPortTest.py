import serial   # serial communication
from subprocess import Popen, PIPE

ports = ["COM7", "COM5"]
for port in ports:
    ser = serial.Serial()
    ser.port=port
    ser.baudrate=115200
    # set parity and ...

#serialobjects.append(ser)

# call subprocess
# pass the serial object to subprocess
# read out serial port


# HOW TO PASS SERIAL OBJECT HERE to stdin
p1 = Popen(['python', './ReadCOM.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE) # read COM1 permanently
p2 = Popen(['python', './ReadCOM.py'], stdin=PIPE, stdout=PIPE, stderr=PIPE) # read COM2 permanently

for i in range(10):
    print("recieved from COM1: %s" % p1.stdout.readline()) # print output from ReadCOM.py for COM1
    print("received from COM2: %s" % p2.stdout.readline()) # print output from ReadCOM.py for COM2