import ASCOMDriver as ASCOM
import time
from Mount import Mount

mount = Mount("/dev/tty.usbserial-AQ00LYCP",9600, 5)
mount.slew_to_mech_zero()




