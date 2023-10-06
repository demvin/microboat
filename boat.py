import network

import machine
import gc
from time import sleep
import time
from micropython import const
import vincenty
import gps
import compass
import comms
import ecran

#import bno08x_find_heading

position = {"lat" : None, "lng" : None, "yaw": None, "heading": None, "speed": None} #lat, lng

stations = "zozo"


# A WLAN interface must be active to send()/recv()
#sta = network.WLAN(network.STA_IF)
#sta.active(True)
#sta.config(channel=1)
#sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

#print(sta.config('mac'))

_THROTTLE_INVALID = const(5000)
_THROTTLE_VALID = const(1000)
_THROTTLE_PRINTSTATIONS = _THROTTLE_VALID

sleep(2)


# 
# 

comms.init()
gps.init()
compass.init()


def main():
    global position
    
    print("main")
    
    
    last_sent = time.ticks_ms()
    last_no_msg = time.ticks_ms()
    last_print_stations = time.ticks_ms()
    last_print_head = time.ticks_ms()

    bootmsg = "BOOT|{now}".format(now = last_sent)
    print("-> " + bootmsg)
    comms.broadcast(bootmsg)
    del bootmsg

    while True:
        sleep(0.1)
        
        dist = None
            
        g = gps.acquire()
        if g:
            #print("GPS:" + str(gps.position))
            position['lat'] = gps.position['lat']
            position['lng'] = gps.position['lng']
        
        comp = compass.acquire()
        if(comp):
            heading = compass.heading
            #print(heading)
            if heading is not None:
                position['yaw'] = str(heading[0])
            else:
                position['yaw'] = None
            
        if comms.acquire():
            pass
            #print(comms.stations)
        
            
#             if time.ticks_diff(time.ticks_ms(), last_print_head) > 5000: 
#                 outhead = "GPH|{}|{}|{}".format(heading[0], heading[1],heading[2])
#                 print("-> " + outhead)
#                 e.send(bcast, outhead, False)
#                 last_print_head = time.ticks_ms()


        if time.ticks_diff(time.ticks_ms(), last_print_stations) > _THROTTLE_PRINTSTATIONS: 
            for k in list(comms.stations.keys()):
                v = comms.stations[k]
                v["a"] = time.ticks_diff(time.ticks_ms(), v["r"]) / 1000
                if v["a"] > 10:
                    print("ejecting " + str(k))
                    del comms.stations[k]
                else:                   
                    print(k,v)
                    
            last_print_stations = time.ticks_ms()            

        
        ecran.update('info', position, comms.stations)
    

main()

