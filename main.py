import network, time
from machine import RTC

print("waiting")
time.sleep(1)
print("not waiting")


def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
  sta = network.WLAN(network.STA_IF); sta.active(False)
  ap = network.WLAN(network.AP_IF); ap.active(False)
  
  sta.active(True)
  sta.config(channel=1)
  
  # required weird fix to prevent crash on startup
  ap.active(False)
  sta.active(True)
  
  while not sta.active():
      time.sleep(0.1)
  
  sta.disconnect()   # For ESP8266
  while sta.isconnected():
      time.sleep(0.1)
  
  return sta, ap


#c = RTC()

#/if c.datetime()[5] % 2 == 0:
print("resseting")
wifi_reset()
print("radio reset")
import boat




