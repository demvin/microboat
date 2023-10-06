


from time import sleep
import gc

print("debug break point")
sleep(5)

bo = bytearray(b'\x02')

for i in range(0,10000):
    ##print(i)
    bo.extend(b'\x02\x03\x04\x05' * 3)
    print("l:" + str(len(bo)))
    print("mf:" + str(gc.mem_free()))
    #sleep(0.1)

