from micropyGPS import MicropyGPS
from machine import UART

my_gps = None
uart1 = None

def default_position():
    return {'lat': None, 'lng': None, 'head': None, 'speed': None}

position = default_position()


def init():
    global my_gps
    global uart1
    
    uart1 = UART(1, baudrate=9600, tx=33, rx=32)
    my_gps = MicropyGPS(0, 'dd')
   
    
def acquire():
    global position
    
    if uart1.any():

        for b in uart1.read():
            stat = my_gps.update(chr(b)) # Note the conversion to to chr, UART outputs ints normally
            if not stat:
                pass
            else:
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
                
                st = "GP{v}|{t}|{lat}|{lon}|{spd}|{head}".format(v=str(my_gps.valid)[0],
                    t=datefix, lat=my_gps.latitude[0], lon=my_gps.longitude[0] * -1, spd=my_gps.speed[2],
                    head=my_gps.course
                )
                
                if my_gps.valid:                    
                    position['lat'] = my_gps.latitude[0]
                    position['lng'] = my_gps.longitude[0] * -1
                else:
                    del position
                    position = default_position()
                
                return True
                
                #if time.ticks_diff(time.ticks_ms(), last_sent) > delay: 
                #    print("-> " + st)
                #    e.send(bcast, st, False)
#                   
                    #last_sent = time.ticks_ms()
#                     print("data sent")
    else:
        return False
