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

    return [altaz, altlimit, ser]


def driver(alt, az):
    #  Alt/az should be input as 8 character .01 arcsecond (idk exactly what this means)
    #  Also could convert this within function
    # define serial port being used  (dependant on Pi number)

    notused1, notused2, ser = setup()

    alt = str(alt)
    az = str(az)

    ser.write(":Sas" + alt + "#")  # define command altitude
    ser.write(":Sz" + az + "#")  # define command azimuth

    ser.write(":MS#")  # command to slew to defined coordinates
    ser.write(":ST1#")  # command to start tracking


def calibrate():
    notused1, notused2, ser = setup()

    ser.write(":Q#")  # stop slewing
    ser.write(":ST0#")  # stop tracking
    ser.write(":CM#")  # command to calibrate



