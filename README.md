This turns a Beaglebone Black into a power button.

It uses a Tornado server to create a simple web interface to trigger a relay:
* Relay is on P9_41
* Button is on P8_7 and is default HIGH (LOW on click)

Other bits:
* uses supervisord to run power.py as root (Adafruit_BBIO requires root)
* cron has a sample of the rtunnel.sh script we run on cron for remote SSH access
* /etc/network/interfaces includes wifi setup 
