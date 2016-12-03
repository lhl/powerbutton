#!/usr/bin/env python

# see https://github.com/numato/samplecode/blob/master/RelayAndGPIOModules/USBRelayAndGPIOModules/python/usbrelay1_2_4_8/relaywrite.py

import sys
import serial
import time

# https://github.com/numato/samplecode/blob/master/RelayAndGPIOModules/USBRelayAndGPIOModules/python/usbrelay1_2_4_8/relayread.py


if (len(sys.argv) == 1):
  print('Defaulting to /dev/ttyACM0 and GPIO pin 7')
  portName = '/dev/ttyACM0'
  relayNum = 3
elif (len(sys.argv) == 2):
  portName = '/dev/ttyACM0'
  relayNum = sys.argv[1];
else:
  portName = sys.argv[1];
  relayNum = sys.argv[2];


#Open port for communication  
serPort = serial.Serial(portName, 19200, timeout=1)

while True:
  command = "gpio read "+ str(relayNum) + "\n\r"
  command = command.encode('ascii')
  serPort.write(command)
  response = serPort.read(25)
  print(response.decode('ascii'))
  if(response.decode('ascii').find("on") > 0):
    print("on")
  
time.sleep(0.5)

#Close the port
serPort.close()
