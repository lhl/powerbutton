import Adafruit_BBIO.GPIO as GPIO
import time
 
GPIO.setup("P9_41", GPIO.OUT)

GPIO.output("P9_41", GPIO.HIGH)
time.sleep(5.3)
GPIO.output("P9_41", GPIO.LOW)

GPIO.cleanup()



