import time
from Mount import Mount
from GSM import GSM

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)
gsm = GSM("/dev/tty.usbserial-AQ00LYCP",9600, 5)
number = '+1XXXXXXXXXX'

gsm.set_to_sms()
msg = gsm.read_msg(0,0)
if msg == "Start":
    while True:
        cmd = gsm.read_msg(0, 0)
        time.sleep(3)
        if cmd[0] == '0':
            # RA/Dec Command
            # format: 0<hhmmss><+/-><xxx>.<xxxx><hhmmss>
            ra = cmd[1:6]
            # parse to get to seconds
            hrs = ra[0:1]
            minutes = ra[2:3]
            sec = ra[3:5]
            ra = float(hrs)*3600 + float(minutes)*60 + float(sec)

            dec = float(cmd[7:15])
            t = cmd[16:21]  # this might need to be typecast

            # handle time stuff
            mount.set_ra_dec(ra, dec)
            mount.slew_to_coordinates()

            # camera stuff here

            # astrometry/image processing
        if cmd[0] == '1':
            # NORAD ID Command
            # format: 1<XXXXX(5-digit NORAD ID)><hhmmss>
            n_id = cmd[1:5]
            t = cmd[6:11]

            # Propagator magic
            alt = 3  # result of propagator magic
            az = 3  # result of propagator magic
            # handle time stuff
            mount.set_alt_az(alt, az)
            mount.slew_to_coordinates()

            # camera stuff here

            # astrometry/image processing

        # send stuff back to CCAR
        # format: <hhmmss><+/-><xxx>.<xxxx><hhmmss><hhmmss><+/-><xxx>.<xxxx><hhmmss>
        msg_out = 'something'  # this comes from image processing

        gsm.send_sms(number, msg_out)
