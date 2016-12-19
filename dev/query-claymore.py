import json
from   pprint import pprint
import requests

r = requests.get('http://devbox.local:3333/')
text = r.text.split('<br>')
text = text[0].split('{')
j = json.loads('{' + text[1])
(hashrate, shares, rejected) = j['result'][2].split(';')
if int(hashrate) <= 50000:
  print('low hashrate')
