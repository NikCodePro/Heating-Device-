from machine import Pin,I2C,UART
from urtc import DS1307
ser = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1),timeout = 500)
while 1 :
    data = ser.read(1)
    if data == None:
        pass
    else :
        data = data.decode('utf-8')
        char = ord(data)
        print(char,data)
#         if data == "*" :
#             print("delete pressed")
#         if data == "\n" :
#             print("enter pressed")