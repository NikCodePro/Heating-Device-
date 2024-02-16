from machine import I2C, Pin,UART
from urtc import DS1307
import time

i2c1 = I2C(0,scl = Pin(13),sda = Pin(12),freq = 400000)
rtc = DS1307(i2c1)
ser = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13),timeout = 500)
# year = int(input("Year : "))
# month = int(input("month (Jan --> 1 , Dec --> 12): "))
# date = int(input("date : "))
# day = int(input("day (1 --> monday , 2 --> Tuesday ... 0 --> Sunday): "))
# hour = int(input("hour (24 Hour format): "))
# minute = int(input("minute : "))
# second = int(input("second : "))
# 
# now = (year,month,date,day,hour,minute,second,0)
# rtc.datetime(now)

while True:
    data = ser.read()
    print(data)
    time.sleep(1)
    #(year,month,date,day,hour,minute,second,p1)=rtc.datetime()
    #utime.sleep(1)
    #print(rtc.datetime())