#!/usr/bin/python


import datetime
import json
import logging
from   multiprocessing import Process, Queue
import os
import requests
import socket
import subprocess
import sys
import time


HOME = os.path.dirname(os.path.realpath(__file__))

# Logging
FORMAT = '%(asctime)-15s : %(levelname)s : %(message)s'
logging.basicConfig(filename='{}/log/watchdog.log'.format(HOME),level=logging.INFO,format=FORMAT)

if sys.stdout.isatty():
  console = logging.StreamHandler()
  console.setLevel(logging.INFO)
  formatter = logging.Formatter(FORMAT)
  console.setFormatter(formatter)
  logging.getLogger('').addHandler(console)

logging.info('START watchdog')

# Socket Timeout
socket.setdefaulttimeout(0.5)

# If up or down
is_up = True

# Timestampe since Down
down_since = 0.0


def dns_lookup(host, q):
  try:
    socket.gethostbyname(host)
    q.put('OK')
  except:
    pass


if socket.gethostname() == 'powerbutton':
  target = 'oregon.local'
else:
  target = 'devbox.local'

while 1:
  start = time.time()

  # Check if it's online
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # DNS lookup
    q = Queue()
    p = Process(target=dns_lookup, args=(target, q,))
    p.start()
    time.sleep(0.4)

    if q.empty():
      p.terminate()
      if is_up:
        is_up = False
        down_since = time.time()
    else:
      if not is_up:
        logging.info('BACK UP after {:.2f} s'.format(down_since))
        is_up = True
        down_since = 0.0
  except socket.error as e:
    if is_up:
      is_up = False
      down_since = time.time()

  # Check if it's hashing
  if is_up:
    if target == 'devbox.local':
      try:
        r = requests.get('http://devbox.local:3333/')
        text = r.text.split('<br>')
        text = text[0].split('{')
        j = json.loads('{' + text[1])
        (hashrate, shares, rejected) = j['result'][2].split(';')
        if int(hashrate) <= 50000:
          logging.info('LOW HASHRATE: {}'.format(hashrate))
          is_up = False
          if not down_since:
            down_since = time.time()
      except:
        logging.info('DOWN: Claymore miner unreachable')
        is_up = False
        down_since = time.time()

      
  # If down, then let's potentially reboot this thing...
  if not is_up:
    if down_since > 0 and time.time() - down_since > 60:
      # OK, let's reboot this sucker
      logging.info('DOWN {:.2f} s, REBOOTING'.format(down_since))
      subprocess.call(['{}/bin/hard-reset'.format(HOME)])
      # Reset Down - as long as it doesn't take more than 80s to come up we should be fine
      down_since = time.time()


  # Try to sleep to 1s
  sleep = (start+1) - time.time() - 0.001
  if sleep > 0:
    time.sleep(sleep)
