import RPi.GPIO as GPIO
import serial

# define button number
buttonNum = 3  # customize for how we wire the Pi


def setup():
    # GPIO.setmode(GPIO.BOARD)  # sets board as mode
    # GPIO.setup(buttonNum, GPIO.IN, GPIO.PUD_UP)  # defines button, input, and pull up (not sure what that last one
    # means)

    # define serial port being used  (dependant on Pi number)
    ser_port = "/dev/ttyUSB0"  # defining serial port as using USB (Linux standard)

    # define settings
    ser = serial.Serial(ser_port, 9600, timeout=5)
    altaz = ser.write(":GAC#")  # check current alt-az
    altlimit = ser.write(":GAL#")  # check altitude limit

    ser.write(':RT0#')  # set sidereal tracking
    ser.write("SG-360")  # set timezone
    ser.write(":SDS0#")  # not DST

    return [altaz, altlimit]


def driver(alt, az):
    #  Alt/az should be input as 8 character .01 arcsecond (idk exactly what this means)
    #  Also could convert this within function
    # define serial port being used  (dependant on Pi number)
    ser_port = "/dev/ttyUSB0"  # defining serial port as using USB (Linux standard)

    # define settings
    ser = serial.Serial(ser_port, 9600, timeout=5)

    ser.write(":SasTTTTTTTT#")  # define command altitude
    ser.write(":SzTTTTTTTTT#")  # define command azimuth




