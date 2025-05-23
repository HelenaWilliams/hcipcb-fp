import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/cu.usbmodem4827E2FD7CA02'
ser.open()


while True:
    print(ord(ser.read(1)))
