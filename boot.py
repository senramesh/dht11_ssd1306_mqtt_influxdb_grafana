# Boot up and Connect to WiFi

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

#import esp
#esp.debug(None)

import gc
gc.collect()

ssid = 'YOUR-SSID'
password = 'YOUR-WIFI-PASSWORD'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())
