import Adafruit_BBIO.GPIO as GPIO
import time
 
GPIO.setup("P8_7", GPIO.IN)

while 1:
  if GPIO.input("P8_7"):
    print("HIGH")
  else:
    print("LOW")
  time.sleep(0.1)

GPIO.cleanup()
