import serial
import time, sys
import datetime

"""# define button number
buttonNum = 3  # customize for how we wire the Pi


def setup():
    GPIO.setmode(GPIO.BOARD)  # sets board as mode
    GPIO.setup(buttonNum, GPIO.IN, GPIO.PUD_UP)  # defines button, input, and pull up (not sure what that last one
    # means)


def statusreport():
    # define serial port being used  (dependant on Pi number)
    ser_port = "/dev/ttyUSB0"  # defining serial port as using USB (Linux standard)

    # define settings
    ser = serial.Serial(ser_port, 9600, timeout=5)
    setup()
    ser.write("AT+CMGF=1\r")  # set to text mode
    time.sleep(3)  # set sleep timer
    ser.write('AT+CMGDA="DEL ALL"\r')  # delete all SMS
    time.sleep(3)
    reply = ser.read(ser.inWaiting())  # Define reply with SMS cleared

    while True:
        reply = ser.read(ser.inWaiting())
        if reply != "":  # if reply isn't blank
            ser.write("AT+CMGR=1\r")  # command to read SMS
            time.sleep(3)
            reply = str(ser.read(ser.inWaiting()))
            if "GSMStatus" in reply:
                t = str(datetime.datetime.now())  # time using datetime library

                # time/location using GSM
                # Long/lat in degrees, date format:  YYYY/MM/DD, time zone: GMT, time format: hh/mm/ss
                [locationcode, long, lat, gsmdate, gsmtime] = ser.write("AT+CIPGSMLOC=1\r")
                ser.write('AT+CMGS="+1XXXXXXXXXX"\r')  # send SMS to given phone number
                time.sleep(3)
                if locationcode == 0:
                    msg = "GPS date and time: " + gsmdate + gsmtime + "GPS Location: " + "Longitude: " + long + "Latitude: " + lat
                if locationcode == 404:
                    msg = "Not Found"
                if locationcode == 408:
                    msg = "Request Timed Out"
                if locationcode == 601:
                    msg = "Network Error"
                if locationcode == 602:
                    msg = "No Memory"
                if locationcode == 603:
                    msg = "DNS Error"
                if locationcode == 604:
                    msg = "Stack Busy"
                if locationcode == 65535:
                    msg = "Other Error"
                else:
                    msg = "Error: no Location Code"
                ser.write(msg)
            time.sleep(3)
            ser.write('AT+CMGDA="DEL ALL"\r')  # delete all SMS
            time.sleep(3)
            ser.read(ser.inWaiting())  # clear buf
        time.sleep(5)


def datasend(msg):
    # define serial port being used  (dependant on Pi number)
    ser_port = "/dev/ttyUSB0"  # defining serial port as using USB (Linux standard)

    # define settings
    ser = serial.Serial(ser_port, 9600, timeout=5)
    setup()
    ser.write("AT+CMGF=1\r")  # set to text mode
    time.sleep(3)  # set sleep timer
    ser.write('AT+CMGDA="DEL ALL"\r')  # delete all SMS
    time.sleep(3)

    # set msg to string
    str(msg)

    ser.write('AT+CMGS="+1XXXXXXXXXX"\r')  # send SMS to given phone number
    time.sleep(3)
    ser.write(msg)
    time.sleep(5)


def dataread():
    # define serial port being used  (dependant on Pi number)
    ser_port = "/dev/ttyUSB0"  # defining serial port as using USB (Linux standard)

    # define settings
    ser = serial.Serial(ser_port, 9600, timeout=5)
    setup()
    ser.write("AT+CMGF=1\r")  # set to text mode
    time.sleep(3)  # set sleep timer
    ser.write('AT+CMGDA="DEL ALL"\r')  # delete all SMS
    time.sleep(3)

    while True:
        reply = ser.read(ser.inWaiting())
        if reply != "":  # if reply isn't blank
            ser.write("AT+CMGR=1\r")  # command to read SMS
            time.sleep(3)
            reply = str(ser.read(ser.inWaiting()))
            if "NORAD ID" in reply:
                # NORAD ID stuff
            if "RA/Dec" in reply:
                # RA/Dec stuff
            time.sleep(3)
            ser.write('AT+CMGDA="DEL ALL"\r')  # delete all SMS
            time.sleep(3)
            ser.read(ser.inWaiting())  # clear buf
        time.sleep(5)"""

packet = '<locationcode>[,<longitude>,<latitude>,<date>,<time>]'
locationcode = packet[0:packet.find("[")]
packet = packet[packet.find(',')+1:-1] + ']'
gsm_long = packet[0:packet.find(',')]
packet = packet[packet.find(',')+1:-1] + ']'
gsm_lat = packet[0:packet.find(',')]
packet = packet[packet.find(',')+1:-1] + ']'
gsm_date = packet[0:packet.find(',')]
packet = packet[packet.find(',')+1:-1] + ']'
gsm_time = packet[0:-1]