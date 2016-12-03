#!/usr/bin/env python

# see https://github.com/numato/samplecode/blob/master/RelayAndGPIOModules/USBRelayAndGPIOModules/python/usbrelay1_2_4_8/relaywrite.py

import sys
import serial
import time


if (len(sys.argv) == 1):
  print('Defaulting to /dev/ttyACM0 and GPIO pin 7')
  portName = '/dev/ttyACM0'
  relayNum = 0
elif (len(sys.argv) == 2):
  portName = '/dev/ttyACM0'
  relayNum = sys.argv[1];
else:
  portName = sys.argv[1];
  relayNum = sys.argv[2];


#Open port for communication  
serPort = serial.Serial(portName, 19200, timeout=1)

#Send the command
command = "relay on "+ str(relayNum) + "\n\r"
command = command.encode('ascii')
serPort.write(command)

time.sleep(0.3)

command = "relay off "+ str(relayNum) + "\n\r"
command = command.encode('ascii')
serPort.write(command)

#Close the port
serPort.close()
