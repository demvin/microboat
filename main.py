import network, time

def do_connect():
    import network
    
    sta_if = network.WLAN(network.STA_IF)
    sta_if.config(channel=1)
    sleep(1)
    sta_if.active(True)
    sleep(1)
    #if not sta_if.isconnected():
    #    print('connecting to network...')
        
    #sta_if.connect('Happier Place', 'karine123')
    sta_if.disconnect()
    #if sta_if.isconnected():
        #    pass
    print('network config:', sta_if.ifconfig())
    #import webtest
 
def oo_connect():
    
    sta_if = network.WLAN(network.STA_IF)
        
    sta_if.active(True)
    sta_if.config(channel=1)
    sta_if.disconnect()
    
    #if not sta_if.isconnected():
    #    print('connecting to network...')
        
    #sta_if.connect('Happier Place', 'karine123')
    
    #if sta_if.isconnected():
        #    pass
    print('network config:', sta_if.ifconfig()) 
 


def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
  sta = network.WLAN(network.STA_IF); sta.active(False)
  ap = network.WLAN(network.AP_IF); ap.active(False)
  sta.config(channel=1)
  sta.active(True)
  while not sta.active():
      time.sleep(0.1)
  sta.disconnect()   # For ESP8266
  while sta.isconnected():
      time.sleep(0.1)
  return sta, ap

#sta, ap = wifi_reset()
 
#oo_connect()
wifi_reset()
print("fin")
#import boat


