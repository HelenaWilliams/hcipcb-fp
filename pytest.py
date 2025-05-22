import pylink
import time
jlink = pylink.JLink()
jlink.open(serial_no=801015138)
print(jlink.product_name)
print(jlink.opened())
jlink.rtt_start()
while True:
    print(jlink.rtt_read(0, 100))
    time.sleep(100)


jlink.rtt_stop()