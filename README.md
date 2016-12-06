# Summary
This turns a Beaglebone Black into a power button.

It uses a Tornado server to create a simple web interface to trigger a relay:
* Relay is on P9_41
* Button is on P8_7 and is default HIGH (LOW on click)

Other bits:
* uses supervisord to run power.py as root (Adafruit_BBIO requires root)
* cron has a sample of the rtunnel.sh script we run on cron for remote SSH access
* /etc/network/interfaces includes wifi setup (not included in repo)

Note, on a BBB (ubuntu image) you will need to install `libnss-mdns` and make sure you append `mdns` to the end of the `hosts` stanza in `/etc/nsswitch.conf` to resolve mdns

# License
   Copyright 2016 Leonard Lin

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
