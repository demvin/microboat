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
from bno08x_rvc import BNO08x_RVC, RVCReadTimeoutError

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


uart2 = UART(2, baudrate=115200, rx=27, tx=22)
rvc = BNO08x_RVC(uart2, timeout=1)

def main():
    print("main")
    last_sent = time.ticks_ms()
    last_no_msg = time.ticks_ms()
    last_print_stations = time.ticks_ms()
    last_print_head = time.ticks_ms()

    bootmsg = "BOOT|{now}".format(now = last_sent)
    print("-> " + bootmsg)
    e.send(bcast, bootmsg , False)
    del bootmsg

    while True:
        heading = None
        dist = None
        
        try:
            heading = rvc.heading
            #direction = get_compass_point(yaw)
            #offset = get_offset(yaw, direction)
            #print("{} {}".format(direction, offset))
            if time.ticks_diff(time.ticks_ms(), last_print_head) > 5000: 
                outhead = "GPH|{}|{}|{}".format(heading[0], heading[1],heading[2])
                print("-> " + outhead)
                e.send(bcast, outhead, False)
                last_print_head = time.ticks_ms()

        except RVCReadTimeoutError:
            heading = None

        msg = None
        host, msg = e.recv(0)
        
        if msg:             # msg == None if timeout in recv()
            #print(host, msg)
            msg = str(msg, "uft-8")
            msg = validate(msg)
            
            if(msg):
               
                val = stations.get(str(host),{})
                val["r"] = time.ticks_ms()
                
                ar = msg.split('|')
                
                if ar == None or len(ar) < 1:
                    continue
                
                val["last"] = ar[0]
                
                if ar[0] == "GPF":
                    val["dist"] = None
                    val["lat"] = None
                    val["lng"] = None
                elif ar[0] == "GPT":
                    if len(ar) > 2:            
                        lat = float(ar[2])
                        lng = float(ar[3])
                        dist = vincenty.vincenty(maison, (lat, lng))
                        val["dist"] = dist
                        val["lat"] = lat
                        val["lng"] = lng
                    else:
                        lan = lng = dist = None
                        val["dist"] = None
                        val["lat"] = None
                        val["lng"] = None
                elif ar[0] == "GPH":
                   val["h"] = ar[1]
                elif ar[0] == "BOOT":
                    pass
                else:
                    print("unknown packet type: {}".format(ar[0]))

                stations[str(host)] = val                
                     
            #time.sleep_ms(100)
                

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
                        print("-> " + st)
                        e.send(bcast, st, False)
    #                     print(my_gps.gps_segments[3] or "NODATA")
    #                     print(my_gps.gps_segments[5] or "NODATA")
    #                     time.sleep(2)
                        
                        last_sent = time.ticks_ms()
    #                     print("data sent")
    
def validate(msg):
    return msg

main()

