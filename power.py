#!/usr/bin/env python


import Adafruit_BBIO.GPIO as GPIO
import time
import tornado.ioloop
import tornado.web


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

    tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Try: <a href='/click'>/click</a> or <a href='/hold'>/hold</a>")


class ClickHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("CLICK!")
    GPIO.output("P9_41", GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output("P9_41", GPIO.LOW)


class HoldHandler(tornado.web.RequestHandler):
  def get(self):
    self.write("Holding for 5s ... ")
    self.flush()
    GPIO.output("P9_41", GPIO.HIGH)
    time.sleep(5.3)
    GPIO.output("P9_41", GPIO.LOW)
    self.write("OK!")


def button_listener():
  # Note this is synchronous so we don't have to worry about any interference from HTTP or vice versa
  if GPIO.input("P8_7"):
    GPIO.output("P9_41", GPIO.LOW)
  else:
    # print("CLICK")
    GPIO.output("P9_41", GPIO.HIGH)


if __name__ == "__main__":
  print "Starting Power Button Server on Port 80"
  Application().listen(80)

  # Initialize GPIO
  GPIO.setup("P9_41", GPIO.OUT)
  GPIO.setup("P8_7", GPIO.IN)

  try:
    tornado.ioloop.PeriodicCallback(button_listener, 100).start()
    tornado.ioloop.IOLoop.current().start()
  except KeyboardInterrupt:
    # Graceful shutdown: 
    # http://stackoverflow.com/questions/22314234/pyzmq-tornado-ioloop-how-to-handle-keyboardinterrupt-gracefully
    # https://gist.github.com/mywaiting/4643396
    GPIO.cleanup()
