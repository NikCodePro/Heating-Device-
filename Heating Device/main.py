from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from machine import Pin, I2C, UART
from urtc import DS1307
import time
# import ads1x15
import sys
import uos
import ubinascii

addr = 72
gain = 1

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(1, sda=machine.Pin(10), scl=machine.Pin(11), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
Button_Data = Pin(14, Pin.IN, Pin.PULL_UP)
Button_Menu = Pin(17, Pin.IN, Pin.PULL_UP)
buzzer = Pin(27, Pin.OUT)
pin_OUT = Pin(28, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(22, Pin.OUT)
i2c1 = I2C(0, scl=Pin(13), sda=Pin(12), freq=400000)
rtc = DS1307(i2c1)
# ads_1115 = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
# ads = ads1x15.ADS1115(ads_1115, addr, gain)
# keyboard TX/Rx
ser = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), timeout=100)
sim = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # Assuming Pico's UART 0
CPU_SERIAL = "e6616408436a8031"
printLine1Counter = -1
isShowingMenu = 0
isTransferringFile = 0
value = 0
val = 0
savee = 0
avg_tare = 20
avg_val = 5
current_time = 0
pdName = '4CC8-90D'
masterPassword = 'etlmd'
calibPassword = 'calib'
C_ET = int(time.time())
lcd.clear()
lcd.putstr("WELCOME TO ETLMD\n LAKSHMI MEERUT")
time.sleep(1)
date = 0
month = 0
year = 0 
hour = 0
minute = 0
pressure = 0


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
        for placeholder, valuet in placeholders.items():
            format_str = format_str.replace(placeholder, f"{valuet:02}")

        return format_str

def show_pressure():
        # read PRESSURE Vals----
#     ads_val = ads.read(4, 0)
#     volts = ads.raw_to_v(ads_val)
    pressure = str(pressure)
    lcd.move_to(0, 0)
    parsedPressure = f"Pressure: 00Bar"
    lcd.putstr(parsedPressure)
    pressure = int(pressure)


def start_timer():
    global year, month, date, day, hour, minute, second, pressure
    # read timer vals----
    N_ET = int(time.time())
    timer = N_ET - C_ET
    t = time.localtime(timer)
    minute = format_time(t, "%M")
    sec = format_time(t, "%S")
    lcd.move_to(0, 1)
    parsedWeight = 'Time: ' + f"{minute[1]}:{sec}"
    lcd.putstr(parsedWeight)


def generate_file(value1):
    print("in generate file")
    try:
        file = open("file.txt", "a+")
    except Exception as e:
        print(e)
        lcd.clear()
        lcd.putstr("file open")
        time.sleep(10)
    try:
        file1 = open("temps.csv", "a+")
    except Exception as e:
        print(e)
        lcd.clear()
        lcd.putstr("temp open")
        time.sleep(10)
    try:
        file.write(str(value1) + "\n")
        file.close()
    except Exception as e:
        print(e)
        lcd.clear()
        lcd.putstr("file save")
        time.sleep(10)
    try:
        file1.write(str(value1) + "\n")
        file1.close()
    except Exception as e:
        print(e)
        lcd.clear()
        lcd.putstr("temp save")
        time.sleep(10)


def DataSaved(Pin):
    global val, savee, value, printLine1Counter
    # print("weight : ",val , "Value : ", savee)
    if (val > 200 and val < 2010 and savee == 0):
        (year, month, date, day, hour, minute, second, p1) = rtc.datetime()
        try:
            file = open("line.txt")
        except Exception as e:
            print(e)
            lcd.clear()
            lcd.putstr("Contact Support")
            time.sleep(10)
        line = file.read()
        file.close()
        try:
            file1 = open("from_tp.txt")
        except Exception as e:
            print(e)
            lcd.clear()
            lcd.putstr("Contact Support")
            time.sleep(10)
        from_tp = file1.read()
        file1.close()
        try:
            file2 = open("to_tp.txt")
        except Exception as e:
            print(e)
            lcd.clear()
            lcd.putstr("Contact Support")
            time.sleep(10)
        to_tp = file2.read()
        file2.close()
        value = getOnLcd(val)
        line3 = "3" + "," + str(getStrictString(str(date), 2, 1)) + "/" + str(getStrictString(str(month), 2, 1)) + "/" + str(getStrictString(str(year), 4, 1)) + "," + str(getStrictString(str(hour), 2, 1)) + ":" + str(
            getStrictString(str(minute), 2, 1)) + "," + value + "," + str(getStrictString(str(line), 4, 0)) + "," + str(getStrictString(str(from_tp), 4, 0)) + "," + str(getStrictString(str(to_tp), 4, 0))
        value1 = str(line3)
        print("DATA ENTERED", value1)
        try:
            generate_file(value1)
        except Exception as e:
            print(e)
            lcd.clear()
            lcd.putstr("error insacing file")
            time.sleep(10)
        print('enter in db and beep')
        buzzer.on()
        time.sleep(1)
        buzzer.off()
        printLine1Counter = 0
        savee = 1


Button_Data.irq(trigger=Pin.IRQ_FALLING, handler=DataSaved)


def toggleMenu(Pin):
    global isShowingMenu, val
    if val < 20:
        if (isShowingMenu == 0):
            isShowingMenu = 1
        else:
            isShowingMenu = 0
    else:
        isShowingMenu = 0


Button_Menu.irq(trigger=Pin.IRQ_FALLING, handler=toggleMenu)


def transferFile(Pin):
    global isTransferringFile
    if (isTransferringFile == 0):
        isTransferringFile = 1
        print('FILE TRANSFER MODE')
    else:
        isTransferringFile = 0


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


def getLine1(editRailway, editDivision, editWelderDetails, editFirmDetails):
    line1 = "1" + "," + str(getStrictString(editRailway, 4, 0)) + "," + str(getStrictString(editDivision, 4, 0)) + \
        "," + str(getStrictString(editWelderDetails, 9, 0)) + \
        "," + str(getStrictString(editFirmDetails, 7, 0))
    value1 = line1
    generate_file(value1)


def getLine2(KP):
    line2 = "2" + "," + str(getStrictString(KP, 4, 1))
    value1 = line2
    generate_file(value1)


def getOnLcd(val):

    val = int(val)
    if (val < 20):
        return '0000'
    elif (val < 100):
        return '00' + str(val)
    elif (val < 1000):
        return '0' + str(val)

    return str(val)


def buttons():
    while True:
        if Button_Data.value() == 0:
            DataSaved(0)
        if Button_Menu.value() == 0:
            toggleMenu(0)


def send_SMS():
    def send_command(cmd):
        sim.write(cmd.encode() + b'\r\n')
        time.sleep(0.1)
        response = sim.read()  # Read up to 64 bytes of response
        return response

    message = "Hello from Raspberry Pi Pico! \nThis message is sent by the SIM8000A Module With Rasberry Pi"
    recipient_numbers = ["+916396176135", "+919258041401", "+919711366959"]  #Add more recipients number
    i = 0
    for i in recipient_numbers:
        send_command("AT")
        send_command('AT+CMGF=1') 
        send_command('AT+CMGS="' + i + '"')
        send_command(message + '\x1A')
        print(f"SMS Sent Succesfully to {i}")

def startTracker():
    global isTransferringFile, isShowingMenu, printLine1Counter, val, avg_tare, avg_val, savee, minutes, seconds, current_time, C_ET, N_ET
    try:
        file = open("reference_unit.txt")
        reference_unit = file.read()
        file.close()
        file1 = open("reference_weight.txt")
        reference_weight = file1.read()
        file1.close()

    # except:
    except Exception as e:
        print(e)
        lcd.clear()
        lcd.putstr("Contact Support")
        # return
    lcd.clear()
    while True:
        (year, month, date, day, hour, minute, second, p1) = rtc.datetime()
        if (isTransferringFile == 0):
            if (isShowingMenu == 0):
                # try:
                val = 0
                if (val > 2000):
                    overload = "OVERLOAD: " + str(val) + ' Kg '
                    lcd.move_to(0, 0)
                    lcd.putstr(overload)
                    lcd.move_to(0, 1)
                    lcd.putstr(str(getStrictString(str(date), 2, 1)) + "/" + str(getStrictString(str(month), 2, 1)) + "/" + str(getStrictString(
                        str(year), 4, 1)) + " " + str(getStrictString(str(hour), 2, 1)) + ":" + str(getStrictString(str(minute), 2, 1)))
                    buzzer.on()

                elif (printLine1Counter >= 0 and printLine1Counter < 200):
                    buzzer.off()
                    savee = 1
                    printLine1Counter += 1
                    ToPrint = "SAVED: " + value + ' Kg  '
                    lcd.move_to(0, 0)
                    lcd.putstr(ToPrint)
                    lcd.move_to(0, 1)
                    lcd.putstr(str(getStrictString(str(date), 2, 1)) + "/" + str(getStrictString(str(month), 2, 1)) + "/" + str(getStrictString(
                        str(year), 4, 1)) + " " + str(getStrictString(str(hour), 2, 1)) + ":" + str(getStrictString(str(minute), 2, 1)))

                else:
                    savee = 0
                    buzzer.off()
                    start_timer()
                    
                # except (KeyboardInterrupt, SystemExit):
                # except Exception as e:
                #     print("ERROR----->", e)
                #     lcd.clear()
                #     lcd.putstr("Contact Support")
                #     # return

            else:
                print('isShowingMenu now')
                lcd.move_to(0, 0)
                lcd.putstr('SET DATE & TIME:')
                lcd.move_to(0, 1)
                currentTime = (str(getStrictString(str(date), 2, 1)) + "/" + str(getStrictString(str(month), 2, 1)) + "/" + str(
                    getStrictString(str(year), 4, 1)) + " " + str(getStrictString(str(hour), 2, 1)) + ":" + str(getStrictString(str(minute), 2, 1)))
                lcd.putstr(currentTime)
                editCurrentTime = currentTime
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
                        # print('char is not int datetime', char)
                        pass
                    elif (char >= 48 and char <= 57 and len(editCurrentTime) <= 15):
                        editCurrentTime = editCurrentTime + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editCurrentTime)
                        if (len(editCurrentTime) == 2 or len(editCurrentTime) == 5):
                            editCurrentTime = editCurrentTime + '/'
                            lcd.move_to(0, 1)
                            lcd.putstr(editCurrentTime)
                        if (len(editCurrentTime) == 10):
                            editCurrentTime = editCurrentTime + ' '
                            lcd.move_to(0, 1)
                            lcd.putstr(editCurrentTime)
                        if (len(editCurrentTime) == 13):
                            editCurrentTime = editCurrentTime + ':'
                            lcd.move_to(0, 1)
                            lcd.putstr(editCurrentTime)

                    elif (key == '*'):
                        print('Yayy backspace pressed datetime')
                        editCurrentTime = editCurrentTime[:-1]
                        print(editCurrentTime)
                        lcd.move_to(0, 1)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("SET DATE & TIME:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editCurrentTime)
                    elif (key == '\n'):
                        print('Enter pressed datetime')
                        if not (editCurrentTime == currentTime):
                            try:
                                dateTime = editCurrentTime
                                print(dateTime)
                                dateTimeArr = dateTime.split(' ')
                                date = dateTimeArr[0]
                                time = dateTimeArr[1]
                                dateArr = date.split('/')
                                timeArr = time.split(':')
                                date = int(dateArr[0])
                                month = int(dateArr[1])
                                year = int(dateArr[2])
                                hour = int(timeArr[0])
                                minute = int(timeArr[1])
                                now = (year, month, date, 1,
                                       hour, minute, 0, 0)
                                rtc.datetime(now)
                                print('success yayyy railway')
                            except Exception as e:
                                print(e)
                        else:
                            # railway name unchanged, nothing to update
                            print('nothing to update pass datetime')
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
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122)) and len(editRailway) < 4):
                        editRailway = editRailway + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editRailway)
                        # lcd.print_line(editRailway, line=1)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editRailway = editRailway[:-1]
                        # print(editRailway)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("RAILWAY NAME :")
                        lcd.move_to(0, 1)
                        lcd.putstr(editRailway)
                        # lcd.print_line(editRailway, line=1)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editRailway == railway):
                            # set new railway name in db
                            file = open("railway.txt", "w")
                            file.write(str(editRailway))
                            file.close()
                            # print(file.read())
                            pass
                        else:
                            # railway name unchanged, nothing to update
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
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122)) and len(editDivision) < 4):
                        editDivision = editDivision + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editDivision)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editDivision = editDivision[:-1]
                        # print(editDivision)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("DIVISION NAME :")
                        lcd.move_to(0, 1)
                        lcd.putstr(editDivision)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editDivision == division):
                            # set new division name in db
                            file = open("division.txt", "w")
                            file.write(str(editDivision))
                            # print(editDivision)
                            file.close()
                            pass
                        else:
                            # division name unchanged, nothing to update
                            pass
                        break

                # Welder Details
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("Welder Detail:")
                file = open("Welder_Detail.txt")
                welder_dt = file.read()
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
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122)) and len(editWelderDetails) < 4):
                        editWelderDetails = editWelderDetails + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editWelderDetails)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editWelderDetails = editWelderDetails[:-1]
                        # print(editWelderDetails)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("Welder Details:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editWelderDetails)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editWelderDetails == welder_dt):
                            # set new division name in db
                            file = open("Welder_Details.txt", "w+")
                            file.write(str(editWelderDetails))
                            # print(editWelderDetails)
                            file.close()
                            pass
                        else:
                            # from_station unchanged, nothing to update
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
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122)) and len(editFirmDetails) < 4):
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
                        # print(key)
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
                        # print('Yayy backspace pressed')
                        editKilometerPost = editKilometerPost[:-1]
                        # print(editKilometerPost)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("KILOMETER POST:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editKilometerPost)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editKilometerPost == km):
                            # set new km_post name in db
                            file = open("km_post.txt", "w+")
                            file.write(str(editKilometerPost))
                            # print(editKilometerPost)
                            file.close()
                            getLine2(editKilometerPost)
                            pass
                        else:
                            # km_post unchanged, nothing to update
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
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122) or (char >= 48 and char <= 57)) and len(editLineName) < 4):
                        editLineName = editLineName + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editLineName)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editLineName = editLineName[:-1]
                        # print(editLineName)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("LINE NAME:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editLineName)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editLineName == line):
                            # set new line name name in db
                            file = open("line.txt", "w+")
                            file.write(str(editLineName))
                            # print(editLineName)
                            file.close()
                            pass
                        else:
                            # line name unchanged, nothing to update
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
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122) or (char >= 48 and char <= 57)) and len(editFromTp) < 4):
                        editFromTp = editFromTp + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editFromTp)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editFromTp = editFromTp[:-1]
                        # print(editFromTp)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("FROM TP:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editFromTp)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editFromTp == from_tp):
                            # set new line name name in db
                            file = open("from_tp.txt", "w+")
                            file.write(str(editFromTp))
                            # print(editFromTp)
                            file.close()
                            pass
                        else:
                            # from tp name unchanged, nothing to update
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
                        # print(key)
                    char = ''
                    try:
                        char = ord(key)
                    except:
                        pass

                    if not (isinstance(char, int)):
                        # print('char is not int', char)
                        pass
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122) or (char >= 48 and char <= 57)) and len(editToTp) < 4):
                        editToTp = editToTp + key
                        lcd.move_to(0, 1)
                        lcd.putstr(editToTp)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editToTp = editToTp[:-1]
                        # print(editToTp)
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("TO TP:")
                        lcd.move_to(0, 1)
                        lcd.putstr(editToTp)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        if not (editToTp == to_tp):
                            # set new line name name in db
                            file = open("to_tp.txt", "w+")
                            file.write(str(editToTp))
                            # print(editToTp)
                            file.close()
                            pass
                        else:
                            # to tp name unchanged, nothing to update
                            pass
                        break

                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("DELETE ALL DATA?")
                lcd.move_to(0, 1)
                lcd.putstr("ENTER PASSWORD")
                editMasterPass = ''
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
                    elif (((char >= 65 and char <= 90) or (char >= 97 and char <= 122) or (char >= 48 and char <= 57))):
                        editMasterPass = editMasterPass + key
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("DELETE ALL DATA?")
                        lcd.move_to(0, 1)
                        lcd.putstr(editMasterPass)
                    elif (key == '*'):
                        # print('Yayy backspace pressed')
                        editMasterPass = editMasterPass[:-1]
                        lcd.clear()
                        lcd.move_to(0, 0)
                        lcd.putstr("DELETE ALL DATA?")
                        lcd.move_to(0, 1)
                        lcd.putstr(editMasterPass)
                    elif (key == '\n'):
                        # print('Enter pressed')
                        global masterPassword, calibPassword
                        if (editMasterPass == masterPassword):
                            file = open("file.txt", "w+")
                            file.close()
                            file1 = open("temps.csv", "w+")
                            file1.close()
                            toPrintLine = 1
                            lcd.clear()
                            lcd.move_to(0, 0)
                            lcd.putstr("ALL DATA DELETED")
                            time.sleep(3)
                        elif (editMasterPass == calibPassword):
                            newValues = calibrate(reference_unit, reference_weight)
                            reference_unit = newValues[0]
                            reference_weight = newValues[1]
                            # print("nothing")
                        else:
                            if (len(editMasterPass) > 0):
                                lcd.clear()
                                lcd.move_to(0, 0)
                                lcd.putstr("Wrong cred. try again")
                                editMasterPass = ''
                                lcd.move_to(0, 1)
                                lcd.putstr(editMasterPass)
                                time.sleep(3)
                            pass
                        break

                # in the end set isShowingMenu to false to continue displaying
                lcd.clear()
                lcd.move_to(0, 0)
                lcd.putstr("SUCCESS")
                lcd.move_to(0, 1)
                lcd.putstr("DETAILS UPDATED")
                isShowingMenu = 0
                time.sleep(5)

        else:
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr('SENDING DATA')
            # createAndTransferFiles()
            isTransferringFile = 0


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
        time.sleep(1)
        buzzer.off()
        sys.exit()

# _thread.start_new_thread(buttons, ())


getserial()
startTracker()
