import serial
import time

# define serial port being used  (dependant on Pi number)
#  ser_port = "/dev/ttyUSB0"  # defining serial port as using USB (Linux standard)
serport = "/dev/tty.usbserial-AQ00LYCP"


def setup(ser_port):
    # GPIO.setmode(GPIO.BOARD)  # sets board as mode
    # GPIO.setup(buttonNum, GPIO.IN, GPIO.PUD_UP)  # defines button, input, and pull up (not sure what that last one
    # means)

    print("running setup...")

    #  define settings
    ser = serial.Serial(ser_port, 9600, timeout=5)
    ser.write(b':GAC#')  # check current alt-az
    response = ser.readline()
    packet = response.decode()
    decodealtaz(packet)

    ser.write(b':SAL-89#')
    response = ser.readline()
    packet = response.decode()
    print("New alt limit?: " + packet)

    ser.write(b':GAL#')  # check altitude limit
    response = ser.readline()
    packet = response.decode()
    print("Alt limit: " + packet)

    # ser.write(b':RT0#')  # set sidereal tracking
    # ser.write(b'SG-420')  # set timezone
    # ser.write(b':SDS0#')  # not DST

    # return [altaz, altlimit, ser]


def driver(alt, az):
    #  Alt/az should be input as 8 character .01 arcsecond (idk exactly what this means)
    # define serial port being used  (dependant on Pi number)

    ser = serial.Serial("/dev/tty.usbserial-AQ00LYCP", 9600, timeout=5)

    alt = alt*360000
    alt = round(alt)
    alt = str(alt)
    alt = alt.rjust(8, '0')
    print("Alt input: " + alt)

    az = az*360000
    az = round(az)
    az = str(az)
    az = az.rjust(8, '0')
    print("Az input: " + az)

    ser.write(b':Sas' + alt.encode() + b'#')  # define command altitude
    response = ser.readline()
    packet = response.decode()
    print("Altitude?: " + packet)

    ser.write(b':Sz' + az.encode() + b'#')  # define command azimuth
    response = ser.readline()
    packet = response.decode()
    print("Azimuth?: " + packet)

    ser.write(b':MS#')  # command to slew to defined coordinates
    response = ser.readline()
    packet = response.decode()
    print("Slew to Coordinates?: " + packet)

    time.sleep(10)
    ser.write(b':GAC#')  # check current alt-az
    response = ser.readline()
    packet = response.decode()
    decodealtaz(packet)

    # ser.write(b':ST1#')  # command to start tracking
    # response = ser.readline()
    # packet = response.decode()
    # print(packet)


def calibrate():

    ser.write(b':Q#')  # stop slewing
    ser.write(b':ST0#')  # stop tracking
    ser.write(b':CM#')  # command to calibrate


def zeroposition():
    ser = serial.Serial("/dev/tty.usbserial-AQ00LYCP", 9600, timeout=5)

    # ser.write(b':MSH#')  # search for zero position
    # response = ser.readline()
    # packet = response.decode()
    # print("Position search?: " + packet)
    # time.sleep(10)

    ser.write(b':MH#')  # slew to zero position
    response = ser.readline()
    packet = response.decode()
    print("Zero actuation?: " + packet)


def decodealtaz(inputstr):
    alt = inputstr[0] + str(int(inputstr[1:9])/360000)
    az = str(int(inputstr[10:18])/360000)
    print("Alt: " + alt)
    print("Az: " + az)




