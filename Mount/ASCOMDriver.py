def driver(ra, dec):
    import win32com.client
    mount = win32com.client.Dispatch("mountid")

    if mount.Connected:
        print "Mount already connected"
    else:
        mount.Connected = True
        if mount.Connected:
            print "Connected to mount"
        else:
            print "Unable to connect"

    mount.Tracking = True
    mount.SlewToCoordinates(ra, dec)
    mount.Connected = False

