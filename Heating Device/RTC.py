from machine import I2C, Pin, Timer, ADC
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import utime
import time


I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
# display configuratons
display = I2C(1, sda = Pin(10), scl= Pin(11), freq=400000)
lcd = I2cLcd(display, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

CET = int(time.time())

def format_time(time_struct, format_str):
    # Define mappings for format placeholders
    placeholders = {
        '%Y': time_struct[0],   # Year with century
        '%y': time_struct[0] % 100,  # Year without century
        '%m': time_struct[1],  # Month (01-12)
        '%d': time_struct[2],  # Day of the month (01-31)
        '%H': time_struct[3],  # Hour (00-23)
        '%M': time_struct[4],  # Minute (00-59)
        '%S': time_struct[5],  # Second (00-59)
        '%a': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][time_struct[6]],  # Short day name
        '%b': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][time_struct[1] - 1]  # Short month name
    }

    # Replace format placeholders with corresponding values
    for placeholder, value in placeholders.items():
        format_str = format_str.replace(placeholder, f"{value:02}")

    return format_str


while True:
    NET = int(time.time())
    timer = NET - CET
    t = time.localtime(timer)
    minute = format_time(t, "%M")
    sec = format_time(t, "%S")
    lcd.clear()
    lcd.move_to(4,0)
    lcd.putstr(f"{minute[1]}:{sec}")
    print(f"\r {minute[1]}:{sec}" , end="")
    time.sleep(1)


