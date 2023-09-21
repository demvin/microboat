
def do_connect():
    import network
    
    sta_if = network.WLAN(network.STA_IF)
    sta_if.config(channel=1)
    sta_if.active(True)
    #if not sta_if.isconnected():
    #    print('connecting to network...')
        
    #sta_if.connect('Happier Place', 'karine123')
    sta_if.disconnect()
        #while not sta_if.isconnected():
        #    pass
    print('network config:', sta_if.ifconfig())
    #import webtest
 
do_connect()
import boat
