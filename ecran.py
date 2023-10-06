from machine import Pin, I2C
import ssd1306
import time

display = None
max_dist = 0
last_update = time.ticks_ms()

def init():
    global display
    
    i2c = I2C(0)
    try:
        display = ssd1306.SSD1306_I2C(128, 64, i2c)
        print("lcd inited")
    except:
        print("no led")

def updatePos(pos, stations):
    global last_update
    global max_dist
            
    if display == None or time.ticks_diff(time.ticks_ms(), last_update) < 1000:
        return
    
    display.fill(0)
    display.text('LAT:' + pos['lat'], 0, 0, 1)
    display.text('LNG:' + pos['lng'], 0, 9)
    display.text('YAW:' + pos['yaw'], 0, 18, 1)

    dist = 0
    top = 26
    for k,i in stations.items():
        #print(k,i)
        if 'dist' in i and i['dist'] is not None:
            d = i['dist']
            display.text('Dis:' + str(d) or "0", 0, top, 1)
            if d > max_dist:
                max_dist = d
            
            top = top + 8
    
    display.text('Max:' + str(max_dist) or "0", 0, top, 1)    

    display.show()
    last_update = time.ticks_ms()

# Basic functions:
# 
# display.poweroff()     # power off the display, pixels persist in memory
# display.poweron()      # power on the display, pixels redrawn
# display.contrast(0)    # dim
# display.contrast(255)  # bright
# display.invert(1)      # display inverted
# display.invert(0)      # display normal
# display.rotate(True)   # rotate 180 degrees
# display.rotate(False)  # rotate 0 degrees
# display.show()         # write the contents of the FrameBuffer to display memory
# 
# display.fill(0)
# display.fill_rect(0, 0, 32, 32, 1)
# display.fill_rect(2, 2, 28, 28, 0)
# display.vline(9, 8, 22, 1)
# display.vline(16, 2, 22, 1)
# display.vline(23, 8, 22, 1)
# display.fill_rect(26, 24, 2, 4, 1)
# display.text('MicroPython', 40, 0, 1)
# display.text('SSD1306', 40, 12, 1)
# display.text('OLED 128x64', 40, 24, 1)
# display.show()


# display.fill(0)                         # fill entire screen with colour=0
# display.pixel(0, 10)                    # get pixel at x=0, y=10
# display.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1
# display.hline(0, 8, 4, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
# display.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1
# display.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
# display.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
# display.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
# display.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
# display.scroll(20, 0)                   # scroll 20 pixels to the right
# 
# # draw another FrameBuffer on top of the current one at the given coordinates
# import framebuf
# fbuf = framebuf.FrameBuffer(bytearray(8 * 8 * 1), 8, 8, framebuf.MONO_VLSB)
# fbuf.line(0, 0, 7, 7, 1)
# display.blit(fbuf, 10, 10, 0)           # draw on top at x=10, y=10, key=0
# display.show()

#display.fill(0)
# display.fill_rect(0, 0, 32, 32, 1)
# display.fill_rect(2, 2, 28, 28, 0)
# display.vline(9, 8, 22, 1)
# display.vline(16, 2, 22, 1)
# display.vline(23, 8, 22, 1)
# display.fill_rect(26, 24, 2, 4, 1)
# display.text('MicroPython', 40, 0, 1)
# display.text('SSD1306', 40, 12, 1)
# display.text('OLED 128x64', 40, 24, 1)
# display.show()
