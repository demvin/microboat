from bno08x_rvc import BNO08x_RVC, RVCReadTimeoutError
from machine import UART

heading = None

uart2 = None
rvc = None


def init():
    global uart2
    global rvc
    
    uart2 = UART(2, baudrate=115200, rx=27, tx=22)
    rvc = BNO08x_RVC(uart2, timeout=1)

def acquire():
    global heading
    
    try:
        heading = rvc.heading
        return True
    except:
        return False
    
    
    