import Adafruit_BBIO.GPIO as GPIO
import time
 

GPIO.setup("P9_41", GPIO.OUT)

while 1:
  GPIO.output("P9_41", GPIO.HIGH)
  time.sleep(1)
  GPIO.output("P9_41", GPIO.LOW)
  time.sleep(1)

GPIO.cleanup()



