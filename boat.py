import network
import espnow
from machine import UART
import machine
import gc
from time import sleep
from micropyGPS import MicropyGPS
import time
from micropython import const
import vincenty

#import bno08x_find_heading

bcast = const(b'\xff') * 6

maison = (45, -73)

my_gps = MicropyGPS(0, 'dd')

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

uart1 = UART(1, baudrate=9600, tx=33, rx=32)

stations = {}

e = espnow.ESPNow()
e.active(True)
peer = bcast   # MAC address of peer's wifi interface
try:
    e.add_peer(peer, channel=1)
#    e.add_peer(b'\x10\x97\xbd\xd440', channel=1)
#    e.add_peer(b'\x10\x97\xbd\xd5h@', channel=1)
#    e.add_peer(b'\x10\x97\xbd\xd5h', channel=1)
except:
    pass


def main():
    print("main")
    last_sent = time.ticks_ms()
    last_no_msg = time.ticks_ms()
    last_print_stations = time.ticks_ms()

    e.send(bcast, "$BOOT|{now}".format(now = last_sent), False)

    while True:
        msg = None
        host, msg = e.recv(0)
        
        if msg:             # msg == None if timeout in recv()
            #print(host, msg)
            msg = str(msg)
            msg = validate(msg)
            
            if(msg):
                ar = msg.split('|')
                
                if len(ar) > 2:            
                    lat = float(ar[2])
                    lng = float(ar[3])
                    dist = vincenty.vincenty(maison, (lat, lng))
                else:
                    lan = lng = dist = None
                
                
                stations[str(host)] = {"last": ar, "dist": dist, "r": time.ticks_ms()}
                #time.sleep_ms(100)
            else:
                print("wasted")
                
            #print(stations)
        else:
            pass
            #print("no msg")
            #delay = _THROTTLE_INVALID

        if time.ticks_diff(time.ticks_ms(), last_print_stations) > _THROTTLE_PRINTSTATIONS: 
            for k in list(stations.keys()):
                v = stations[k]
                v["a"] = time.ticks_diff(time.ticks_ms(), v["r"]) / 1000
                if v["a"] > 10:
                    print("ejecting " + str(k))
                    del  stations[k]
                else:                   
                    print(k,v)
                    
            last_print_stations = time.ticks_ms()            

        if uart1.any():

            for b in uart1.read():
                stat = my_gps.update(chr(b)) # Note the conversion to to chr, UART outputs ints normally
                if stat:
                    stat = None
    #                 print('UTC Timestamp:', my_gps.timestamp)
    #                 print('Date:', my_gps.date_string('long'))
    #                 print('Latitude:', my_gps.latitude_string())
    #                 print('Longitude:', my_gps.longitude_string())
    #                 print('Horizontal Dilution of Precision:', my_gps.hdop)
    #                 print()
                    
                    datefix = "20{y}{m:02d}{d:02d}T{h:02}{mm:02}{s:02d}".format(y = my_gps.date[2],
                                                             m = my_gps.date[1],
                                                             d = my_gps.date[0],
                                                             h = my_gps.timestamp[0],
                                                             mm = my_gps.timestamp[1],
                                                             s = int(my_gps.timestamp[2]))
                    
                    st = "GP{v}|{t}|{lat}|-{lon}|{spd}|{head}".format(v=str(my_gps.valid)[0],
                        t=datefix, lat=my_gps.latitude[0], lon=my_gps.longitude[0], spd=my_gps.speed[2],
                        head=my_gps.course
                    )
                    
                    if my_gps.valid:
                        delay = _THROTTLE_VALID
                    else:
                        delay = _THROTTLE_INVALID
                    
                    if time.ticks_diff(time.ticks_ms(), last_sent) > delay: 
                        print(st)
                        e.send(bcast, st, False)
    #                     print(my_gps.gps_segments[3] or "NODATA")
    #                     print(my_gps.gps_segments[5] or "NODATA")
    #                     time.sleep(2)
                        
                        last_sent = time.ticks_ms()
    #                     print("data sent")
    
def validate(msg):
    return msg

main()
