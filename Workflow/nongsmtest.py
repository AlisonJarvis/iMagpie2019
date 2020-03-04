import time
from Mount import Mount
from GSM import GSM
import taskHelper
import datetime
from datetime import timedelta

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)
number = '+1XXXXXXXXXX'


def workflowtest(cmd):

        if cmd[0] == '0':
            # RA/Dec Command
            # format: 0<hhmmss><+/-><xxx>.<xxxx><hhmmss>
            ra = cmd[1:6]
            # parse to get to seconds
            hrs = ra[0:1]
            minutes = ra[2:3]
            sec = ra[3:5]
            ra = float(hrs) * 3600 + float(minutes) * 60 + float(sec)

            dec = float(cmd[7:15])
            t = cmd[16:21]  # this might need to be typecast

            # handle time stuff
            mount.set_ra_dec(ra, dec)
            mount.slew_to_coordinates()

            # camera stuff here

            # astrometry/image processing
            return
        if cmd[0] == '1':
            # NORAD ID Command
            # format: 1<XXXXX(5-digit NORAD ID)><hhmmss>
            n_id = cmd[1:5]
            t = cmd[6:11]

            utc_now = datetime.datetime.utcnow()
            LAT = 40.010091
            LONG = -105.243724
            ALT = 1.623974  # km

            # Propagator magic
            az, alt, angrate, exposure_time = taskHelper.findtask(n_id, utc_now, LAT, LONG, ALT)

            # handle time stuff
            mount.set_alt_az(alt, az)
            mount.slew_to_coordinates()

            # camera stuff here

            # astrometry/image processing
            return

        # send stuff back to CCAR
        # format: <hhmmss><+/-><xxx>.<xxxx><hhmmss><hhmmss><+/-><xxx>.<xxxx><hhmmss>
        msg_out = 'something'  # this comes from image processing


# Sample RA/Dec Command
# format: 0<hhmmss><+/-><xxx>.<xxxx><hhmmss>
ra_dec_cmd = '0053654045.1234133033'

# NORAD ID Command
# format: 1<XXXXX(5-digit NORAD ID)><hhmmss>
NORAD_cmd = '125544133033'

# mount.slew_to_mech_zero()
# time.sleep(15)

# ra/dec test
#workflowtest(ra_dec_cmd)
mount.current_ra_dec()

time.sleep(10)

# NORAD ID test
workflowtest(NORAD_cmd)
mount.current_alt_az()

