import espnow
from micropython import const
import time

bcast = const(b'\xff') * 6
stations = {}

e = None

def init():
    global e
    
    e = espnow.ESPNow()
    e.active(True)
    
    try:
        e.add_peer(bcast, channel=1)
    #    e.add_peer(b'\x10\x97\xbd\xd440', channel=1)
    #    e.add_peer(b'\x10\x97\xbd\xd5h@', channel=1)
    #    e.add_peer(b'\x10\x97\xbd\xd5h', channel=1)
    except:
        pass

def validate(msg):
    return msg

def acquire():

    msg = None
    host, msg = e.recv(0)

    if msg is None:
        return False # msg == None if timeout in recv()
        #print(host, msg)
    msg = str(msg, "uft-8")
    msg = validate(msg)
        
    if msg is None:
        return False
           
    val = stations.get(str(host),{})
    val["r"] = time.ticks_ms()
    
    ar = msg.split('|')
            
    if ar == None or len(ar) < 1:
        return False
            
    val["last"] = ar[0]
            
    if ar[0] == "GPF":
        val["dist"] = None
        val["lat"] = None
        val["lng"] = None
    elif ar[0] == "GPT":
        if len(ar) > 2:            
            lat = float(ar[2])
            lng = float(ar[3])
            
            #if position['lat'] is not None and position['lng'] is not None:
            #    dist = vincenty.vincenty((position['lat'], position['lng']), (lat, lng))
            #else:
            #    dist = None
            
            #val["dist"] = dist
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
        val["bt"] = time.ticks_ms()
    else:
        print("unknown packet type: {}".format(ar[0]))

    stations[str(host)] = val                
                 
        #time.sleep_ms(100)
def broadcast(data):
    e.send(bcast, data, False)
    