import time,sys,uos,ubinascii,machine,ads1x15
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from machine import Pin,I2C,UART
from urtc import DS1307
Button_Start = Pin(2, Pin.IN, Pin.PULL_UP)
Button_Menu = Pin(13, Pin.IN, Pin.PULL_UP)
Button_Pause = Pin(6, Pin.IN, Pin.PULL_UP)
Button_Reset = Pin(9, Pin.IN, Pin.PULL_UP)
buzzer = Pin(14, Pin.OUT)

ser = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5), timeout=500)
sim = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
addr = 0x48
gain = 1
ads_1115 = I2C(0, scl=Pin(21), sda=Pin(20), freq=300000)
ads = ads1x15.ADS1115(ads_1115, addr, gain)
#rtc = DS1307(ads_1115)
I2C_ADDR = 0x27
i2c = I2C(1, sda=machine.Pin(26), scl=machine.Pin(27), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
CPU_SERIAL = "e6616407e3843431"


lcd.clear()
lcd.move_to(3, 0)
lcd.putstr("WELCOME TO")
lcd.move_to(0, 1)
lcd.putstr("PRE HEAT BLOWER")
time.sleep(2)
lcd.clear()
lcd.putstr(" LAKSHMI MEERUT")
time.sleep(1)

hour = 0
min_timer = 0
limit = "0"
timer_range = 1
factor = 0.28

timer_flag = False
buzzer_flag = False
pause_flag = False
isShowingMenu = 0

C_ET = int(time.time())
lastRecordedTimer = 0
lastRecordedPressure = 0
offset = 0.5
pressure = 0
timer = 0

# initializing SMS module
def send_command(command):
    print("Sending command:", command)
    try :
        sim.write((command + '\r\n').encode())
        time.sleep(1)
        res =  sim.read().decode()
        print(res)
        if "+CMS ERROR" in res:
            print("network Error")
            lcd.move_to(0,0)
            lcd.putstr("Network_Error..")
            time.sleep(1)
            
    except :
        print("error from send_command")
        lcd.move_to(0,0)
        lcd.putstr("SEND_COMMAND")
        lcd.move_to(0,1)
        lcd.putstr("Check Connection")
        time.sleep(1)
        lcd.clear()
        pass
    
send_command('AT+CMGF=1')
time.sleep(.5)
lcd.clear()

def send_SMS():
    try:
        global  limit, lastRecordedPressure
        lcd.clear()
        lcd.move_to(1, 0)
        lcd.putstr("Sending SMS...")
        with open("railway.txt") as railway_data:
            railway_data = railway_data.read()
        with open("division.txt") as division_data:
            division_data = division_data.read()
        with open("from_tp.txt") as from_tp_data:
            from_tp_data = from_tp_data.read()
        with open("to_tp.txt") as to_tp_data:
            to_tp_data = to_tp_data.read()
        with open("km_post.txt") as km_post_data:
            km_post_data = km_post_data.read()
        with open("line.txt") as line_data:
            line_data = line_data.read()
        with open("Firm_Details.txt") as Firm_Details_data:
            Firm_Details_data = Firm_Details_data.read()
        with open("Welder_Details.txt") as Welder_Details_data:
            Welder_Details_data = Welder_Details_data.read()
        with open("time.txt") as working_time:
            working_time = working_time.read()
        with open("contact1.txt") as number1:
            number1 = number1.read()
        print(number1)
        with open("contact2.txt") as number2:
            number2 = number2.read()
        print(number2)
        with open("contact3.txt") as number3:
            number3 = number3.read()
        print(number3)
        with open("contact4.txt") as number4:
            number4 = number4.read()
        print(number4)
        with open("contact5.txt") as number5:
            number5 = number5.read()
        print(number5)
        with open("contact6.txt") as number6:
            number6 = number6.read()
        print(number6)
        with open("contact7.txt") as number7:
            number7 = number7.read()
        print(number7)
        with open("contact8.txt") as number8:
            number8 = number8.read()
        print(number8)
        with open("contact9.txt") as number9:
            number9 = number9.read()
        print(number9)
        with open("contact10.txt") as number10:
            number10 = number10.read()
        print(number10)
    except:
        print("error open file")
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("error open file")
        lcd.move_to(0,1)
        lcd.putstr("Check file")
        time.sleep(1)
        lcd.clear()
        lcd.move_to(0,0)
        time.sleep(1)
        lcd.clear()
        #pass
    message = f"Rly:{railway_data}\nDivision:{division_data}\nFromTp:{from_tp_data}\nToTp:{to_tp_data}\nKmPost:{km_post_data}\nLine:{line_data}\nPressure:{lastRecordedPressure}Bar\nFirm Detail:{Firm_Details_data}\nWelder Details:{Welder_Details_data}\nTime:{working_time}Min"
    print(len(message))
    if len(number1) >= 10:
        send_sms("+91"+number1, message)
        print("SMS sent to", number1)
    if len(number2) >= 10:
        send_sms("+91"+number2, message)
        print("SMS sent to", number2)
    if len(number3) >= 10:
        send_sms("+91"+number3, message)
        print("SMS sent to", number3)
    if len(number4) >= 10:
        send_sms("+91"+number4, message)
        print("SMS sent to", number4)
    if len(number5) >= 10:
        send_sms("+91"+number5, message)
        print("SMS sent to", number5)
    if len(number6) >= 10:
        send_sms("+91"+number6, message)
        print("SMS sent to", number6)
    if len(number7) >= 10:
        send_sms("+91"+number7, message)
        print("SMS sent to", number7)
    if len(number8) >= 10:
        send_sms("+91"+number8, message)
        print("SMS sent to", number8)
    if len(number9) >= 10:
        send_sms("+91"+number9, message)
        print("SMS sent to", number9)
    if len(number10) >= 10:
        send_sms("+91"+number10, message)
        print("SMS sent to", number10)
    print("All SMS sent successfully.")
    lcd.clear()
    lcd.move_to(1, 0)
    lcd.putstr("SMS Sent")
    time.sleep(1)
    lcd.clear()

# Function to send an SMS
def send_sms(phone_number, message):
    send_command('AT+CMGS="{}"'.format(phone_number))
    time.sleep(0.5)
    send_command(message + chr(26))
    time.sleep(1.5)

def format_time(time_struct, format_str):
    # Define mappings for format placeholders
    placeholders = {
        '%Y': time_struct[0],   # Year with century
        '%y': time_struct[0] % 100,  # Year without century
        '%m': time_struct[1],  # Month (01-12)
        '%d': time_struct[2],  # Day of the month (01-31)
        '%H': time_struct[3],  # Hour (00-23)
        '%M': time_struct[4],  # minutes (00-59)
        '%S': time_struct[5],  # Second (00-59)
        # Short day name
        '%a': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][time_struct[6]],
        # Short month name
        '%b': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][time_struct[1] - 1]
    }

    # Replace format placeholders with corresponding values
    for placeholder, valuet in placeholders.items():
        format_str = format_str.replace(placeholder, f"{valuet:02}")

    return format_str

def get_avg(variable, mean):
    i = 0
    average = 0
    while (i < mean):
        average += variable
        i += 1
    avg = average / mean
    return avg

def show_pressure():
    global offset, factor, lastRecordedPressure, pressure, timer_flag, buzzer_flag
    try:
        adc = ads.read(1, 0)
        volts = ads.raw_to_v(adc)
        volts = int(volts * 100) / 100
        offsetVolts = int((volts - 0.49) * 100) / 100
        pressure = int((offsetVolts * factor) * 100) / 100
        if pressure > 0.20:
            pressure += 0.07
        if pressure > 0.3:
            pressure += 0.02
        if pressure > 0.40:
            pressure += 0.01
        if pressure > 0.50:
            pressure += 0.03
        if not buzzer_flag:
            lcd.move_to(0, 0)
            parsedPressure = f"Pressure:{get_Strict_String(str(pressure), pressure, 4)}Bar"
            lcd.putstr(parsedPressure)
            pressure = float(pressure)
            if timer_flag:
                lastRecordedPressure = pressure
        else:
            lcd.putstr("")
    except:
        lcd.clear()
        print("Error")
        lcd.move_to(0,0)
        lcd.putstr("Sensor Not Read")
        lcd.move_to(0,1)
        lcd.putstr("Check wiring")
        time.sleep(1)
        lcd.clear()
        pass

def timer_flag_run(Pin):
    global C_ET, timer_flag, pause_flag
    if timer_flag == False:
        C_ET = int(time.time())
        timer_flag = True

    if pause_flag:
        C_ET = int(time.time())
        pause_flag = False

def toggleMenu(Pin):
    global isShowingMenu, timer_flag
    if not timer_flag:
        if (isShowingMenu == 0):
            isShowingMenu = 1
        else:
            isShowingMenu = 0

def pause_timer(Pin):
    global pause_flag, C_ET, min_timer, sec
    C_ET = int(time.time())
    if not pause_flag:
        pause_flag = True
        min_timer = 0
        sec = 0
        
def reset_timer(Pin):
    global timer_flag, buzzer_flag, min_timer, sec, C_ET, timer
    
    if timer_flag == True:
        C_ET = int(time.time())
        timer_flag = False
        min_timer = 0
        sec = 0
        timer = 0
        
    # stop buzzer
    if buzzer_flag:
        buzzer_flag = False
        buzzer.off()
        
        # sending sms
        send_SMS()
        
    
def start_timer():
    global day, hour, min_timer, second, pressure, limit, timer, timer_range, timer_flag, buzzer_flag, char, timer, N_ET, C_ET, lastRecordedTimer
    with open("time.txt", "r") as timetxt:
        timer_range = timetxt.read()
        timer_range = int(timer_range)
    if min_timer < timer_range:
        if timer_flag:
            if not pause_flag:
                # read timer vals----
                N_ET = int(time.time())
                timer = (N_ET - C_ET) + lastRecordedTimer
                t = time.localtime(timer)
                min_timer = format_time(t, "%M")
                sec = format_time(t, "%S")
                lcd.move_to(0, 1)
                lcd.putstr('Time: ' + f"{min_timer}:{sec}")
                min_timer = int(min_timer)
                sec = int(sec)
            else:
                lastRecordedTimer = timer
                lcd.move_to(0, 1)
                lcd.putstr('Time:' + f"PAUSED")
                print("lastRecordedTimer====", lastRecordedTimer)
        else:
            lcd.move_to(0, 1)
            lcd.putstr('Time: ' + f"00:00")
            lastRecordedTimer = 0
    else:
        lcd.move_to(0, 0)
        lcd.putstr("Press Reset.....")
        lcd.move_to(0, 1)
        lcd.putstr("Timer Over!")
        lastRecordedTimer = 0
        buzzer_flag = True
        buzzer.on()

def getStrictString(string, reqLen, isNumber):
    actLen = len(string)
    reqString = string

    if (isNumber):
        if (reqLen - actLen == 5):
            reqString = '00000' + reqString
        elif (reqLen - actLen == 4):
            reqString = '0000' + reqString
        elif (reqLen - actLen == 3):
            reqString = '000' + reqString
        elif (reqLen - actLen == 2):
            reqString = '00' + reqString
        elif (reqLen - actLen == 1):
            reqString = '0' + reqString
    else:
        if (reqLen - actLen == 5):
            reqString = '     ' + reqString
        elif (reqLen - actLen == 4):
            reqString = '    ' + reqString
        elif (reqLen - actLen == 3):
            reqString = '   ' + reqString
        elif (reqLen - actLen == 2):
            reqString = '  ' + reqString
        elif (reqLen - actLen == 1):
            reqString = ' ' + reqString
    return reqString

def get_Strict_String(string, p_val3 ,reqlen):
    actLen = len(string)
    reqString = string
    
    if p_val3 >= 0:
        if (reqlen - actLen == 1):
            reqString = reqString[0:3] + "0"
        elif (reqlen - actLen == 0):
            reqString = reqString[0:4]
        elif (reqlen - actLen) <= 2:
            reqString = reqString[0:4]
            
    if p_val3 < 0:
        if (reqlen - actLen == 0):
            reqString = reqString[1:] + "0"
        elif (reqlen - actLen == -1):
            reqString = reqString[1:]
        
    return reqString

def buttons():
    if Button_Start.value() == 0:
        timer_flag_run(Pin)
    if Button_Pause.value() == 0:
        pause_timer(Pin)
    if Button_Menu.value() == 0:
        toggleMenu(Pin)
    if Button_Reset.value() == 0:
        reset_timer(Pin)

def startTracker():
    global isShowingMenu, printLine1Counter, val, minutes, seconds,pressure
    try:
        while True:
            buttons()
            if (isShowingMenu == 0):
                show_pressure()
                start_timer()
            # Showing Menu        
            else:
                print('isShowingMenu now')
                # Set timer
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter timer:")
                file = open("time.txt")
                limit = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(limit)
                lcd.move_to(4, 1)
                lcd.putstr("Minutes")
                editlimit = limit
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editlimit) < 2)):
                        editlimit = editlimit + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editlimit)
                    elif (key == '*'):
                        editlimit = editlimit[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter timer:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editlimit)
                        lcd.move_to(4, 1)
                        lcd.putstr("Minutes")
                    elif (key == '\n'):
                        if not (editlimit == limit):
                            file = open("time.txt", "w+")
                            file.write(str(editlimit))
                            file.close()
                            pass
                        else:
                            pass
                        break
                # Enter mobile Numbers
                # edit line 1
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 1")
                file = open("contact1.txt")
                line1 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line1)
                editline1 = line1
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline1) < 10)):
                        editline1 = editline1 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline1)
                    elif (key == '*'):
                        editline1 = editline1[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 1")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline1)
                    elif (key == '\n'):
                        if not (editline1 == line1):
                            file = open("contact1.txt", "w+")
                            file.write(f'{editline1}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 2
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 2")
                file = open("contact2.txt")
                line2 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line2)
                editline2 = line2
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline2) < 10)):
                        editline2 = editline2 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline2)
                    elif (key == '*'):
                        editline2 = editline2[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 2")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline2)
                    elif (key == '\n'):
                        if not (editline2 == line2):
                            file = open("contact2.txt", "w+")
                            file.write(f'{editline2}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 3
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 3")
                file = open("contact3.txt")
                line3 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line3)
                editline3 = line3
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline3) < 10)):
                        editline3 = editline3 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline3)
                    elif (key == '*'):
                        editline3 = editline3[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 3")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline3)
                    elif (key == '\n'):
                        if not (editline3 == line3):
                            file = open("contact3.txt", "w+")
                            file.write(f'{editline3}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 4
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 4")
                file = open("contact4.txt")
                line4 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line4)
                editline4 = line4
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline4) < 10)):
                        editline4 = editline4 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline4)
                    elif (key == '*'):
                        editline4 = editline4[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 4")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline4)
                    elif (key == '\n'):
                        if not (editline4 == line4):
                            file = open("contact4.txt", "w+")
                            file.write(f'{editline4}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 5
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 5")
                file = open("contact5.txt")
                line5 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line5)
                editline5 = line5
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline5) < 10)):
                        editline5 = editline5 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline5)
                    elif (key == '*'):
                        editline5 = editline5[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 5")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline5)
                    elif (key == '\n'):
                        if not (editline5 == line5):
                            file = open("contact5.txt", "w+")
                            file.write(f'{editline5}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # edit line 6
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 6")
                file = open("contact6.txt")
                line6 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line6)
                editline6 = line6
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline6) < 10)):
                        editline6 = editline6 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline6)
                    elif (key == '*'):
                        editline6 = editline6[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 6")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline6)
                    elif (key == '\n'):
                        if not (editline6 == line6):
                            file = open("contact6.txt", "w+")
                            file.write(f'{editline6}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 7
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 7")
                file = open("contact7.txt")
                line7 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line7)
                editline7 = line7
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline7) < 10)):
                        editline7 = editline7 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline7)
                    elif (key == '*'):
                        editline7 = editline7[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 7")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline7)
                    elif (key == '\n'):
                        if not (editline7 == line7):
                            file = open("contact7.txt", "w+")
                            file.write(f'{editline7}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 8
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 8")
                file = open("contact8.txt")
                line8 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line8)
                editline8 = line8
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline8) < 10)):
                        editline8 = editline8 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline8)
                    elif (key == '*'):
                        editline8 = editline8[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 8")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline8)
                    elif (key == '\n'):
                        if not (editline8 == line8):
                            file = open("contact8.txt", "w+")
                            file.write(f'{editline8}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 9
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 9")
                file = open("contact9.txt")
                line9 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line9)
                editline9 = line9
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline9) < 10)):
                        editline9 = editline9 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline9)
                    elif (key == '*'):
                        editline9 = editline9[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 9")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline9)
                    elif (key == '\n'):
                        if not (editline9 == line9):
                            file = open("contact9.txt", "w+")
                            file.write(f'{editline9}')
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Enter mobile Numbers
                # edit line 10
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Enter SMS no. 10")
                file = open("contact10.txt")
                line10 = file.read()
                file.close()
                lcd.move_to(0, 1)
                lcd.putstr(line10)
                editline10 = line10
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editline10) < 10)):
                        editline10 = editline10 + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editline10)
                    elif (key == '*'):
                        editline10 = editline10[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Enter SMS no. 10")
                        lcd.move_to(0, 1)
                        lcd.putstr(editline10)
                    elif (key == '\n'):
                        if not (editline10 == line10):
                            file = open("contact10.txt", "w+")
                            file.write(f'{editline10}')
                            file.close()
                            pass
                        else:
                            pass
                        break        
                # railway name
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("RAILWAY NAME :")
                file = open("railway.txt")
                railway = file.read()
                file.close()
                print(railway)
                lcd.move_to(0, 1)
                lcd.putstr(railway)
                editRailway = railway
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 65 and char <= 90) and len(editRailway) < 4):
                        editRailway = editRailway + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editRailway)
                    elif (key == '*'):
                        editRailway = editRailway[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("RAILWAY NAME :")
                        lcd.move_to(0, 1)
                        lcd.putstr(editRailway)
                    elif (key == '\n'):
                        if not (editRailway == railway):
                            file = open("railway.txt", "w")
                            file.write(str(editRailway))
                            file.close()
                            pass
                        else:
                            pass
                        break

                # division name
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("DIVISION NAME :")
                file = open("division.txt")
                division = file.read()
                file.close()
                print(division)
                lcd.move_to(0, 1)
                lcd.putstr(division)
                editDivision = division
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90)) and len(editDivision) < 4):
                        editDivision = editDivision + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editDivision)
                    elif (key == '*'):
                        editDivision = editDivision[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("DIVISION NAME :")
                        lcd.move_to(0, 1)
                        lcd.putstr(editDivision)
                    elif (key == '\n'):
                        if not (editDivision == division):
                            file = open("division.txt", "w")
                            file.write(str(editDivision))
                            file.close()
                            pass
                        else:
                            pass
                        break

                # Welder Details
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Welder Detail:")
                file = open("Welder_Details.txt")
                welder_dt = file.readline()
                file.close()
                print(welder_dt)
                lcd.move_to(0, 1)
                lcd.putstr(welder_dt)
                editWelderDetails = welder_dt
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass
                    try:
                        set1 = int(editWelderDetails[0:2])
                    except:
                        pass
                    if set1 == 01:
                        if not (isinstance(char, int)):
                            # print('char is not int', char)
                            pass
                        elif (((char >= 65 and char <= 90) or (char >= 48 and char <= 57)) and len(editWelderDetails) < 9):
                            if ((char >= 48 and char <= 57) and len(editWelderDetails) < 6):
                                editWelderDetails = editWelderDetails + key
                                lcd.move_to(0, 1)
                                lcd.putstr(editWelderDetails)
                            elif((char >= 65 and char <= 90) and len(editWelderDetails) >= 6):
                                editWelderDetails = editWelderDetails + key
                                lcd.move_to(0, 1)
                                lcd.putstr(editWelderDetails)
                        elif (key == '*'):
                            editWelderDetails = editWelderDetails[:-1]
                            lcd.clear()
                            lcd.move_to(0, 0)
                            lcd.putstr("Welder Details:")
                            lcd.move_to(0, 1)
                            lcd.putstr(editWelderDetails)
                        elif (key == '\n'):
                            if not (editWelderDetails == welder_dt):
                                file = open("Welder_Details.txt", "w+")
                                file.write(str(editWelderDetails))
                                file.close()
                                pass
                            else:
                                pass
                            break
                    else:
                        if not (isinstance(char, int)):
                            # print('char is not int', char)
                            pass
                        elif (((char >= 65 and char <= 90) or (char >= 48 and char <= 57)) and len(editWelderDetails) < 7):
                            if ((char >= 48 and char <= 57) and len(editWelderDetails) < 6):
                                editWelderDetails = editWelderDetails + key
                                lcd.move_to(0, 1)
                                lcd.putstr(editWelderDetails)
                            elif((char >= 65 and char <= 90) and len(editWelderDetails) >= 6):
                                editWelderDetails = editWelderDetails + key
                                lcd.move_to(0, 1)
                                lcd.putstr(editWelderDetails)

                        elif (key == '*'):
                            editWelderDetails = editWelderDetails[:-1]
                            lcd.clear()
                            lcd.move_to(0, 0)
                            lcd.putstr("Welder Details:")
                            lcd.move_to(0, 1)
                            lcd.putstr(editWelderDetails)
                        elif (key == '\n'):
                            if not (editWelderDetails == welder_dt):
                                file = open("Welder_Details.txt", "w+")
                                file.write(str(editWelderDetails))
                                file.close()
                                pass
                            else:
                                pass
                            break

                # Firm details
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Firm Details:")
                file = open("Firm_Details.txt")
                firm_dt = file.read()
                file.close()
                print(firm_dt)
                lcd.move_to(0, 1)
                lcd.putstr(firm_dt)
                editFirmDetails = firm_dt
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122)) and len(editFirmDetails) < 16):
                        editFirmDetails = editFirmDetails + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editFirmDetails)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editFirmDetails = editFirmDetails[:-1]
                        # print(editFirmDetails)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Firm Details:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editFirmDetails)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editFirmDetails == firm_dt):
                            # set new division name in db
                            file = open("Firm_Details.txt", "w+")
                            file.write(str(editFirmDetails))
                            # print(editFirmDetails)
                            file.close()
                            pass
                        else:
                            # to_stationunchanged, nothing to update
                            pass
                        break
                if (editFirmDetails != firm_dt) or (editWelderDetails != welder_dt) or (editDivision != division) or (editRailway != railway):
                    getLine1(editRailway, editDivision,
                            editWelderDetails, editFirmDetails)
                    print("PARAMS CHANGED!!!!!!!!")
                    pass
                else:
                    print("NOTHING CHANGED")
                    pass

                # KILOMETER POST
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("KILOMETER POST:")
                file = open("km_post.txt")
                km = file.read()
                file.close()
                print(km)
                lcd.move_to(0, 1)
                lcd.putstr(km)
                editKilometerPost = km
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif ((char >= 48 and char <= 57) and (len(editKilometerPost) < 4)):
                        editKilometerPost = editKilometerPost + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editKilometerPost)
                    elif (key == '*'):
                        editKilometerPost = editKilometerPost[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("KILOMETER POST:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editKilometerPost)
                    elif (key == '\n'):
                        if not (editKilometerPost == km):
                            file = open("km_post.txt", "w+")
                            file.write(str(editKilometerPost))
                            file.close()
                            pass
                        else:
                            pass
                        break

                # LINE NAME
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("LINE NAME:")
                file = open("line.txt")
                line = file.read()
                file.close()
                print(line)
                lcd.move_to(0, 1)
                lcd.putstr(line)
                editLineName = line
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 48 and char <= 57)) and len(editLineName) < 4):
                        editLineName = editLineName + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editLineName)
                    elif (key == '*'):
                        editLineName = editLineName[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("LINE NAME:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editLineName)
                    elif (key == '\n'):
                        if not (editLineName == line):
                            file = open("line.txt", "w+")
                            file.write(str(editLineName))
                            file.close()
                            pass
                        else:
                            pass
                        break

                # FROM TP
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("FROM TP:")
                file = open("from_tp.txt")
                from_tp = file.read()
                file.close()
                print(from_tp)
                lcd.move_to(0, 1)
                lcd.putstr(from_tp)
                editFromTp = from_tp
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                        print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 48 and char <= 57)) and len(editFromTp) < 4):
                        editFromTp = editFromTp + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editFromTp)
                    elif (key == '*'):
                        editFromTp = editFromTp[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("FROM TP:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editFromTp)
                    elif (key == '\n'):
                        if not (editFromTp == from_tp):
                            file = open("from_tp.txt", "w+")
                            file.write(str(editFromTp))
                            file.close()
                            pass
                        else:
                            pass
                        break

                # TO TP
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("TO TP:")
                file = open("to_tp.txt")
                to_tp = file.read()
                file.close()
                print(to_tp)
                lcd.move_to(0, 1)
                lcd.putstr(to_tp)
                editToTp = to_tp
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 48 and char <= 57)) and len(editToTp) < 4):
                        editToTp = editToTp + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editToTp)
                    elif (key == '*'):
                        editToTp = editToTp[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("TO TP:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editToTp)
                    elif (key == '\n'):
                        if not (editToTp == to_tp):
                            file = open("to_tp.txt", "w+")
                            file.write(str(editToTp))
                            file.close()
                            pass
                        else:
                            pass
                        break

                # in the end set isShowingMenu to false to continue displaying
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("DETAILS UPDATED")
                lcd.move_to(0, 1)
                lcd.putstr("Press Enter")
                while 1:
                    key = ser.read(1)
                    if key == None:
                        pass
                    else:
                        key = key.decode('utf-8')
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass
                    if (key == '\n'):
                        pass
                        break

                isShowingMenu = 0
    except:
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Error in Program")
        lcd.move_to(0,1)
        lcd.putstr("Software Issue..")
        time.sleep(1)
        lcd.clear()

def getserial():
    ID = machine.unique_id()
    cpuserial1 = ubinascii.hexlify(ID).decode('utf-8')
    print(cpuserial1)
    if cpuserial1 == CPU_SERIAL:
        flagreturn = 1
    else:
        flagreturn = 0
    if flagreturn == 1:
        print("pass")
        pass
    else:
        lcd.clear()
        lcd.putstr("PIRATED SOFTWARE")
        print("Unauthorised access to software!")
        buzzer.on()
        time.sleep(2)
        buzzer.off()
        sys.exit()

getserial()
startTracker()