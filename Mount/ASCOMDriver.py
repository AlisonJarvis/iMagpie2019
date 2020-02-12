import win32com.client
import datetime


def driver(ra, dec):
    mount = win32com.client.Dispatch("mountid")

    if mount.Connected:
        print("Mount already connected")
    else:
        mount.Connected = True
        if mount.Connected:
            print("Connected to mount")
        else:
            print("Unable to connect")

    # deal with time
    # t = datetime.datetime.now()  #time now

    # if tcommand >= t:
    mount.SlewToCoordinates(ra, dec)
    mount.Tracking = True
    mount.Connected = False

