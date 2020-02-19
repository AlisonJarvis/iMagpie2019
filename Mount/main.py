import ASCOMDriver as ASCOM
import time
from Mount import Mount

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)

#mount.stop_slew()
#mount.calibrate()
mount.slew_to_mech_zero()
#mount.set_alt_az(30, 0)
#mount.slew_to_coordinates()
#time.sleep(10)
print(mount.current_alt_az())



