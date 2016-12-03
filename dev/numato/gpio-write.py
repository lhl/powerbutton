#!/usr/bin/env python

import sys
import serial
import time

if (len(sys.argv) == 1):
  print('Defaulting to /dev/ttyACM0 and GPIO pin 7')
  portName = '/dev/ttyACM0'
  gpioNum = '7'
elif (len(sys.argv) == 2):
  portName = '/dev/ttyACM0'
  gpioNum = sys.argv[1];
else:
  portName = sys.argv[1];
  gpioNum = sys.argv[2];


#Open port for communication  
serPort = serial.Serial(portName, 19200, timeout=1)

#Send the command
command = "gpio set "+ str(gpioNum) + "\r"
command = command.encode('ascii')
serPort.write(command)

time.sleep(0.3)

command = "gpio clear "+ str(gpioNum) + "\r"
command = command.encode('ascii')
serPort.write(command)

#Close the port
serPort.close()
