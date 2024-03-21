from machine import I2C, Pin
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
print(i2c.scan())