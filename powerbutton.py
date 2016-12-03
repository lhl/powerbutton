#!/usr/bin/env python


import os
import platform
import sys
import time
import tornado.ioloop
import tornado.web


class bbbSwitch:
  def __init__(self):
    import Adafruit_BBIO.GPIO as GPIO
    GPIO.setup("P9_41", GPIO.OUT)
    GPIO.setup("P8_7", GPIO.IN)

  def button_listener(self):
    # Note this is synchronous so we don't have to worry about any interference from HTTP or vice versa
    if GPIO.input("P8_7"):
      GPIO.output("P9_41", GPIO.LOW)
    else:
      # print("CLICK")
      GPIO.output("P9_41", GPIO.HIGH)



  def click(self, duration=0.3):
    GPIO.output("P9_41", GPIO.HIGH)
    time.sleep(duration)
    GPIO.output("P9_41", GPIO.LOW)

  def shutdown(self):
    GPIO.cleanup()


class numatoSwitch:
  def __init__(self):
    import serial
    self.serial = serial.Serial('/dev/ttyACM0', 19200, timeout=1)

  def button_listener(self):
    pass

  def click(self, duration=0.3):
    on = 'relay on 0 \n\r'
    on = bytes(on.encode('ascii'))
    off = 'relay off 0 \n\r'
    off = bytes(off.encode('ascii'))

    self.serial.write(on)
    time.sleep(duration)
    self.serial.write(off)

  def shutdown(self):
    self.serial.close()


class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/", MainHandler),
      (r"/click", ClickHandler),
      (r"/hold", HoldHandler),
    ]

    settings = {
      'debug': True,
    }

    # Create Switch Based on Platform Detection
    if platform.machine() == 'armv7l':
      self.switch = bbbSwitch()
    else:
      # x86_64
      # could test for ttyACM0 I suppose...
      self.switch = numatoSwitch()

    tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Try: <a href='/click'>/click</a> or <a href='/hold'>/hold</a>")


class ClickHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("CLICK!")
    self.application.switch.click()


class HoldHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Holding for 5s ... ")
    self.flush()
    self.application.switch.click(5.3)
    self.write("OK!")


if __name__ == "__main__":
  if os.getuid() == 0:
    PORT = 80
  else:
    PORT = 8080
  print("Starting Power Button Server on Port " + str(PORT))
  app = Application()
  app.listen(PORT)

  try:
    tornado.ioloop.PeriodicCallback(app.switch.button_listener, 100).start()
    tornado.ioloop.IOLoop.current().start()
  except KeyboardInterrupt:
    # Graceful shutdown: 
    # http://stackoverflow.com/questions/22314234/pyzmq-tornado-ioloop-how-to-handle-keyboardinterrupt-gracefully
    # https://gist.github.com/mywaiting/4643396
    app.switch.shutdown()
    pass
