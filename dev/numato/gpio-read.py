import sys
import serial

if (len(sys.argv) < 2):
  print("Usage: gpioread.py <PORT> <GPIONUM>\nEg: gpioread.py COM1 0")
  sys.exit(0)
else:
  portName = sys.argv[1];
  gpioNum = sys.argv[2];

#Open port for communication	
serPort = serial.Serial(portName, 19200, timeout=1)

# UGH Python 3 https://docs.python.org/3/howto/unicode.html

#Send "gpio read" command
read_cmd = "gpio read "+ str(gpioNum) + "\r"
read_cmd = read_cmd.encode('ascii')
serPort.write(read_cmd)

response = serPort.read(25)
print(response[-4:-3])

if(response[-4:-3] == "1".encode('ascii')):
  print("GPIO " + str(gpioNum) +" is ON")
	
elif(response[-4:-3] == "0".encode('ascii')):
  print("GPIO " + str(gpioNum) +" is OFF")
	
#Close the port
serPort.close()
